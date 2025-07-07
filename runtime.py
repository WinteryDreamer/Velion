from .ast_nodes import *

class Environment(dict):
    def __init__(self, outer=None):
        super().__init__()
        self.outer = outer
    def __getitem__(self, key):
        if key in self:
            return super().__getitem__(key)
        elif self.outer:
            return self.outer[key]
        else:
            raise NameError(f"Variable '{key}' not found")
    def __setitem__(self, key, value):
        super().__setitem__(key, value)

def run(stmts, env=None, local_vars=None):
    if env is None:
        env = Environment()
    if local_vars is None:
        local_vars = set()
    i = 0
    while i < len(stmts):
        stmt = stmts[i]
        result = exec_stmt(stmt, env, local_vars)
        if isinstance(result, tuple) and result[0] == 'RETURN':
            return result[1]
        i += 1

def exec_stmt(stmt, env, local_vars):
    # Built-in doc
    if isinstance(stmt, Doc):
        # Storage docstring in the environment, can be expanded
        env[f'_doc_{getattr(stmt.stmt, "name", id(stmt.stmt))}'] = stmt.text
        return exec_stmt(stmt.stmt, env, local_vars)
    if isinstance(stmt, Print):
        # Supports multiple expressions and separator
        vals = [eval_expr(e, env) for e in stmt.exprs]
        sep = eval_expr(stmt.sep, env) if stmt.sep else ' '
        print(sep.join(str(v) for v in vals))
    elif isinstance(stmt, AssignOp):
        # Natural assignment: add 1 to x, subtract 2 from x, multiply x by 3, divide x by 2
        if not isinstance(stmt.left, Var):
            raise SyntaxError('Left side of assignment must be a variable')
        varname = stmt.left.name
        current = env[varname]
        if stmt.op == 'add':
            env[varname] = current + eval_expr(stmt.right, env)
        elif stmt.op == 'subtract':
            env[varname] = current - eval_expr(stmt.right, env)
        elif stmt.op == 'multiply':
            env[varname] = current * eval_expr(stmt.right, env)
        elif stmt.op == 'divide':
            env[varname] = current / eval_expr(stmt.right, env)
        else:
            raise SyntaxError(f'Unknown assignment operator {stmt.op}')
    elif isinstance(stmt, ForEachDict):
        d = eval_expr(stmt.iterable, env)
        if not isinstance(d, dict):
            raise TypeError('ForEachDict expects a dictionary')
        for k, v in d.items():
            env[stmt.key] = k
            env[stmt.value] = v
            run(stmt.body, env, local_vars.copy())
    elif isinstance(stmt, Input):
        val = input(str(eval_expr(stmt.prompt, env)))
        env['_last_input'] = val
    elif isinstance(stmt, Assign):
        val = eval_expr(stmt.expr, env)
        if hasattr(val, '__call__'):
            val.__name__ = stmt.name
        if stmt.name in local_vars:
            env[stmt.name] = val
        else:
            env[stmt.name] = val
            local_vars.add(stmt.name)
    elif isinstance(stmt, If):
        cond = eval_expr(stmt.cond, env)
        if cond:
            run(stmt.body, env, local_vars.copy())
        elif stmt.else_body:
            run(stmt.else_body, env, local_vars.copy())
    elif isinstance(stmt, ForEach):
        iterable = eval_expr(stmt.iterable, env)
        if not hasattr(iterable, '__iter__'):
            raise TypeError(f"Object {iterable} is not iterable")
        for item in iterable:
            env[stmt.var] = item
            run(stmt.body, env, local_vars.copy())
    elif isinstance(stmt, FuncDef):
        env[stmt.name] = stmt
    elif isinstance(stmt, Call):
        eval_call(stmt, env)
    elif isinstance(stmt, Lambda):
        return stmt
    elif isinstance(stmt, Import):
        filename = eval_expr(stmt.filename, env)
        if not filename.endswith('.vl'):
            filename += '.vl'
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                code = f.read()
            from .lexer import lex
            from .parser import Parser
            tokens = lex(code)
            parser = Parser(tokens)
            stmts = parser.parse()
            run(stmts, env)
        except Exception as e:
            print(f"Erro ao importar {filename}: {e}")
    elif isinstance(stmt, TryCatch):
        try:
            run(stmt.try_body, env, local_vars.copy())
        except Exception:
            run(stmt.catch_body, env, local_vars.copy())
    elif isinstance(stmt, tuple) and stmt[0] == 'RETURN':
        return ('RETURN', eval_expr(stmt[1], env))
    else:
        eval_expr(stmt, env)

def eval_expr(expr, env):
    if isinstance(expr, StringInterpolation):
        # Replace {var} with value from env
        import re
        def replacer(match):
            var = match.group(1)
            return str(env[var]) if var in env else '{' + var + '}'
        return re.sub(r'\{([a-zA-Z_][a-zA-Z0-9_]*)\}', replacer, expr.template)
    if isinstance(expr, Lambda):
        def _lambda(*args):
            local_env = Environment(outer=env)
            for param, arg in zip(expr.params, args):
                local_env[param] = arg
            return run(expr.body, local_env, set(expr.params))
        return _lambda
    if isinstance(expr, Literal):
        return expr.value
    elif isinstance(expr, ListLiteral):
        return [eval_expr(e, env) for e in expr.elements]
    elif isinstance(expr, DictLiteral):
        return {eval_expr(k, env): eval_expr(v, env) for k, v in expr.pairs}
    elif isinstance(expr, Var):
        return env[expr.name]
    elif isinstance(expr, BinOp):
        left = eval_expr(expr.left, env)
        right = eval_expr(expr.right, env)
        op = expr.op
        if op == '..':
            return str(left) + str(right)
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right
        elif op == '>=':
            return left >= right
        elif op == '<=':
            return left <= right
        elif op == '>':
            return left > right
        elif op == '<':
            return left < right
        elif op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        elif op == 'and':
            return bool(left) and bool(right)
        elif op == 'or':
            return bool(left) or bool(right)
        else:
            raise ValueError(f"Unknown operator {op}")
    elif isinstance(expr, Call):
        # Built-in functions
        if expr.callee == 'length':
            return len(eval_expr(expr.args[0], env))
        elif expr.callee == 'to_number':
            return float(eval_expr(expr.args[0], env))
        elif expr.callee == 'to_string':
            return str(eval_expr(expr.args[0], env))
        elif expr.callee == 'min':
            return min(*(eval_expr(arg, env) for arg in expr.args))
        elif expr.callee == 'max':
            return max(*(eval_expr(arg, env) for arg in expr.args))
        elif expr.callee == 'sort':
            return sorted(eval_expr(expr.args[0], env))
        elif expr.callee == 'reverse':
            return list(reversed(eval_expr(expr.args[0], env)))
        elif expr.callee == 'exit':
            import sys; sys.exit(0)
        elif expr.callee == 'wait':
            import time; time.sleep(float(eval_expr(expr.args[0], env)))
        elif expr.callee == 'clear':
            import os; os.system('cls' if os.name == 'nt' else 'clear')
        else:
            return eval_call(expr, env)
    else:
        raise TypeError(f"Unknown expression type {expr}")

def eval_call(call, env):
    if call.callee in env:
        func = env[call.callee]
        if isinstance(func, FuncDef):
            local_env = Environment(outer=env)
            local_vars = set(func.params)
            # Handle optional and variadic arguments
            args = list(call.args)
            params = list(func.params)
            # Fill in defaults
            for i, pname in enumerate(params):
                if i < len(args):
                    local_env[pname] = eval_expr(args[i], env)
                elif pname in getattr(func, 'defaults', {}):
                    local_env[pname] = eval_expr(func.defaults[pname], env)
                else:
                    raise TypeError(f"Function {call.callee} missing required argument: {pname}")
            # Variadic: when thing(a, ...)
            if getattr(func, 'variadic', None):
                local_env['args'] = [eval_expr(arg, env) for arg in args[len(params):]]
            result = run(func.body, local_env, local_vars)
            return result
        else:
            raise TypeError(f"{call.callee} is not a function")
    else:
        raise NameError(f"Function '{call.callee}' not defined")
