from .lexer import lex
from .ast_nodes import *

class Parser:
    def parse_add_to(self):
        self.consume('KEYWORD', 'add')
        value = self.parse_expr()
        self.consume('KEYWORD', 'to')
        var_token = self.consume('IDENT')
        return AssignOp(Var(var_token[1]), 'add', value)

    def parse_subtract_from(self):
        self.consume('KEYWORD', 'subtract')
        value = self.parse_expr()
        self.consume('KEYWORD', 'from')
        var_token = self.consume('IDENT')
        return AssignOp(Var(var_token[1]), 'subtract', value)

    def parse_multiply_by(self):
        self.consume('KEYWORD', 'multiply')
        var_token = self.consume('IDENT')
        self.consume('KEYWORD', 'by')
        value = self.parse_expr()
        return AssignOp(Var(var_token[1]), 'multiply', value)

    def parse_divide_by(self):
        self.consume('KEYWORD', 'divide')
        var_token = self.consume('IDENT')
        self.consume('KEYWORD', 'by')
        value = self.parse_expr()
        return AssignOp(Var(var_token[1]), 'divide', value)
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def peek_ahead(self, n):
        if self.pos + n < len(self.tokens):
            return self.tokens[self.pos + n]
        return ('EOF', '')

    def advance(self):
        self.pos += 1
        return self.tokens[self.pos -1]

    def match(self, *kinds):
        tk = self.peek()
        if tk and tk[0] in kinds:
            return self.advance()
        return None

    def consume(self, kind, value=None):
        tk = self.peek()
        if not tk or tk[0] != kind or (value is not None and tk[1] != value):
            raise SyntaxError(f"Expected {kind} {value if value else ''}, got {tk}")
        return self.advance()

    def parse(self):
        stmts = []
        while self.peek()[0] != 'EOF':
            stmts.append(self.parse_stmt())
        return stmts

    def parse_stmt(self):
        tk = self.peek()
        if tk[0] == 'KEYWORD':
            if tk[1] == 'lambda' or (tk[1] == 'do' and self.peek_ahead(1)[0] == 'PUNCT' and self.peek_ahead(2)[0] == 'IDENT'):
                return self.parse_lambda()
            if tk[1] == 'doc':
                return self.parse_doc()
            if tk[1] == 'try':
                return self.parse_trycatch()
            if tk[1] == 'say':
                return self.parse_print()
            elif tk[1] == 'add':
                return self.parse_add_to()
            elif tk[1] == 'subtract':
                return self.parse_subtract_from()
            elif tk[1] == 'multiply':
                return self.parse_multiply_by()
            elif tk[1] == 'divide':
                return self.parse_divide_by()
            elif tk[1] == 'input':
                return self.parse_input()
            elif tk[1] == 'remember':
                return self.parse_assign()
            elif tk[1] == 'if':
                return self.parse_if()
            elif tk[1] == 'for':
                return self.parse_for()
            elif tk[1] == 'when':
                return self.parse_funcdef()
            elif tk[1] == 'return':
                return self.parse_return()
            elif tk[1] == 'get':
                return self.parse_import()
            else:
                raise SyntaxError(f"Unknown keyword {tk[1]}")
        else:
            return self.parse_expr()

    def parse_lambda(self):
        if self.match('KEYWORD') and self.tokens[self.pos-1][1] == 'lambda':
            # lambda (a, b) -> ... end
            self.consume('PUNCT', '(')
            params = []
            if not (self.peek()[0] == 'PUNCT' and self.peek()[1] == ')'):
                while True:
                    param = self.consume('IDENT')
                    params.append(param[1])
                    if self.peek()[0] == 'PUNCT' and self.peek()[1] == ')':
                        break
                    self.consume('PUNCT', ',')
            self.consume('PUNCT', ')')
            self.consume('PUNCT', '-')
            self.consume('PUNCT', '>')
            body = []
            while True:
                tk = self.peek()
                if tk[0] == 'KEYWORD' and tk[1] == 'end':
                    self.consume('KEYWORD', 'end')
                    break
                body.append(self.parse_stmt())
            return Lambda(params, body)
        elif self.match('KEYWORD') and self.tokens[self.pos-1][1] == 'do':
            # do (a, b) -> ... end
            self.consume('PUNCT', '(')
            params = []
            if not (self.peek()[0] == 'PUNCT' and self.peek()[1] == ')'):
                while True:
                    param = self.consume('IDENT')
                    params.append(param[1])
                    if self.peek()[0] == 'PUNCT' and self.peek()[1] == ')':
                        break
                    self.consume('PUNCT', ',')
            self.consume('PUNCT', ')')
            self.consume('PUNCT', '-')
            self.consume('PUNCT', '>')
            body = []
            while True:
                tk = self.peek()
                if tk[0] == 'KEYWORD' and tk[1] == 'end':
                    self.consume('KEYWORD', 'end')
                    break
                body.append(self.parse_stmt())
            return Lambda(params, body)

    def parse_doc(self):
        self.consume('KEYWORD', 'doc')
        text = self.consume('STRING')[1]
        stmt = self.parse_stmt()
        return Doc(text, stmt)

    def parse_trycatch(self):
        self.consume('KEYWORD', 'try')
        try_body = []
        while True:
            tk = self.peek()
            if tk[0] == 'KEYWORD' and tk[1] == 'if_it_fails':
                self.consume('KEYWORD', 'if_it_fails')
                break
            try_body.append(self.parse_stmt())
        catch_body = []
        while True:
            tk = self.peek()
            if tk[0] == 'KEYWORD' and tk[1] == 'end':
                self.consume('KEYWORD', 'end')
                break
            catch_body.append(self.parse_stmt())
        return TryCatch(try_body, catch_body)

    def parse_import(self):
        self.consume('KEYWORD', 'get')
        filename = self.parse_expr()
        return Import(filename)

    def parse_input(self):
        self.consume('KEYWORD', 'input')
        prompt = self.parse_expr()
        return Input(prompt)

    def parse_return(self):
        self.consume('KEYWORD', 'return')
        expr = self.parse_expr()
        return ('RETURN', expr)

    def parse_print(self):
        self.consume('KEYWORD', 'say')
        exprs = [self.parse_expr()]
        sep = None
        # Allow: say expr, expr, expr with "..." between
        while self.peek() and self.peek()[0] == 'PUNCT' and self.peek()[1] == ',':
            self.consume('PUNCT', ',')
            exprs.append(self.parse_expr())
        # Optional: with "..." between
        if self.peek() and self.peek()[0] == 'KEYWORD' and self.peek()[1] == 'with':
            self.consume('KEYWORD', 'with')
            sep = self.parse_expr()
            if self.peek() and self.peek()[0] == 'KEYWORD' and self.peek()[1] == 'between':
                self.consume('KEYWORD', 'between')
        return Print(exprs, sep)

    def parse_assign(self):
        self.consume('KEYWORD', 'remember')
        expr = self.parse_expr()
        self.consume('KEYWORD', 'as')
        name_token = self.consume('IDENT')
        return Assign(name_token[1], expr)

    def parse_if(self):
        self.consume('KEYWORD', 'if')
        cond = self.parse_condition()
        self.consume('KEYWORD', 'then')
        body = []
        else_body = []
        while True:
            tk = self.peek()
            if tk[0] == 'KEYWORD' and tk[1] == 'end':
                self.consume('KEYWORD', 'end')
                break
            elif tk[0] == 'KEYWORD' and tk[1] == 'else':
                self.consume('KEYWORD', 'else')
                while True:
                    tk2 = self.peek()
                    if tk2[0] == 'KEYWORD' and tk2[1] == 'end':
                        break
                    else_body.append(self.parse_stmt())
                continue
            else:
                body.append(self.parse_stmt())
        return If(cond, body, else_body if else_body else None)

    def parse_for(self):
        self.consume('KEYWORD', 'for')
        self.consume('KEYWORD', 'each')
        var_token = self.consume('IDENT')
        self.consume('KEYWORD', 'in')
        iterable = self.parse_expr()
        self.consume('KEYWORD', 'do')
        body = []
        while True:
            tk = self.peek()
            if tk[0] == 'KEYWORD' and tk[1] == 'end':
                self.consume('KEYWORD', 'end')
                break
            body.append(self.parse_stmt())
        return ForEach(var_token[1], iterable, body)

    def parse_funcdef(self):
        self.consume('KEYWORD', 'when')
        name_token = self.consume('IDENT')
        self.consume('PUNCT', '(')
        params = []
        if not (self.peek()[0] == 'PUNCT' and self.peek()[1] == ')'):
            while True:
                param = self.consume('IDENT')
                params.append(param[1])
                if self.peek()[0] == 'PUNCT' and self.peek()[1] == ')':
                    break
                self.consume('PUNCT', ',')
        self.consume('PUNCT', ')')
        body = []
        while True:
            tk = self.peek()
            if tk[0] == 'KEYWORD' and tk[1] == 'end':
                self.consume('KEYWORD', 'end')
                break
            stmt = self.parse_stmt()
            body.append(stmt)
        return FuncDef(name_token[1], params, body)

    def parse_expr(self, prec=0):
        left = self.parse_primary()
        while True:
            tk = self.peek()
            if not tk:
                break
            prec_table = {
                '..': 1,
                '==': 2, '!=': 2, '>=': 2, '<=': 2, '>': 2, '<': 2,
                '+': 3, '-': 3,
                '*': 4, '/': 4,
            }
            if tk[0] == 'CONCAT':
                op = '..'
                op_prec = prec_table[op]
            elif tk[0] == 'COMPARE':
                op = tk[1]
                op_prec = prec_table[op]
            elif tk[0] in ['PLUS', 'MINUS', 'MULT', 'DIV']:
                op = tk[1]
                op_prec = prec_table[op]
            else:
                break
            if op_prec < prec:
                break
            self.advance()
            right = self.parse_expr(op_prec + 1)
            left = BinOp(left, op, right)
        return left

    def parse_primary(self):
        tk = self.peek()
        if tk[0] == 'NUMBER':
            self.consume('NUMBER')
            val = float(tk[1]) if '.' in tk[1] else int(tk[1])
            return Literal(val)
        elif tk[0] == 'STRING':
            self.consume('STRING')
            # String interpolation: detect {var} inside string
            if '{' in tk[1] and '}' in tk[1]:
                # Use a generic AST node, to be defined in ast_nodes.py
                return StringInterpolation(tk[1])
            return Literal(tk[1])
        elif tk[0] == 'KEYWORD' and tk[1] in ('yes', 'no'):
            self.consume('KEYWORD', tk[1])
            return Literal(True if tk[1] == 'yes' else False)
        elif tk[0] == 'PUNCT' and tk[1] == '[':
            return self.parse_list()
        elif tk[0] == 'LBRACE':
            return self.parse_dict()
        elif tk[0] == 'IDENT':
            self.consume('IDENT')
            if self.peek()[0] == 'PUNCT' and self.peek()[1] == '(': 
                return self.parse_call(tk[1])
            return Var(tk[1])
        elif tk[0] == 'PUNCT' and tk[1] == '(': 
            self.consume('PUNCT', '(')
            expr = self.parse_expr()
            self.consume('PUNCT', ')')
            return expr
        else:
            raise SyntaxError(f"Unexpected token: {tk}")

    def parse_dict(self):
        self.consume('LBRACE')
        pairs = []
        while True:
            if self.peek()[0] == 'RBRACE':
                self.consume('RBRACE')
                break
            key = self.parse_expr()
            self.consume('COLON')
            value = self.parse_expr()
            pairs.append((key, value))
            if self.peek()[0] == 'RBRACE':
                continue
            self.consume('PUNCT', ',')
        return DictLiteral(pairs)

    def parse_list(self):
        self.consume('PUNCT', '[')
        elements = []
        while True:
            if self.peek()[0] == 'PUNCT' and self.peek()[1] == ']':
                self.consume('PUNCT', ']')
                break
            elements.append(self.parse_expr())
            if self.peek()[0] == 'PUNCT' and self.peek()[1] == ']':
                continue
            self.consume('PUNCT', ',')
        return ListLiteral(elements)

    def parse_call(self, name):
        self.consume('PUNCT', '(')
        args = []
        if not (self.peek()[0] == 'PUNCT' and self.peek()[1] == ')'):
            while True:
                args.append(self.parse_expr())
                if self.peek()[0] == 'PUNCT' and self.peek()[1] == ')':
                    break
                self.consume('PUNCT', ',')
        self.consume('PUNCT', ')')
        return Call(name, args)

    def parse_condition(self):
        left = self.parse_expr()
        if self.match('KEYWORD') and self.tokens[self.pos-1][1] == 'is':
            op_words = []
            while self.match('KEYWORD'):
                op_words.append(self.tokens[self.pos-1][1])
                if op_words[-1] in ['than', 'not']:
                    break
            op = ' '.join(op_words)
            right = self.parse_expr()
            ops_map = {
                'greater than': '>',
                'less than': '<',
                'greater than or equal to': '>=',
                'less than or equal to': '<=',
                'equal to': '==',
                'not equal to': '!=',
                'not greater than': '<=',
                'not less than': '>=',
            }
            op_sym = ops_map.get(op, None)
            if not op_sym:
                raise SyntaxError(f"Unknown operator '{op}'")
            return BinOp(left, op_sym, right)
        else:
            return left
