class ForEachDict:
    def __init__(self, key, value, iterable, body):
        self.key = key
        self.value = value
        self.iterable = iterable
        self.body = body
class AssignOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
class StringInterpolation:
    def __init__(self, template):
        self.template = template
class Lambda:
    def __init__(self, params, body):
        self.params = params
        self.body = body

class Doc:
    def __init__(self, text, stmt):
        self.text = text
        self.stmt = stmt
class TryCatch:
    def __init__(self, try_body, catch_body):
        self.try_body = try_body
        self.catch_body = catch_body
class Import:
    def __init__(self, filename):
        self.filename = filename
class DictLiteral:
    def __init__(self, pairs):
        self.pairs = pairs

class Input:
    def __init__(self, prompt):
        self.prompt = prompt

class Literal:
    def __init__(self, value):
        self.value = value

class ListLiteral:
    def __init__(self, elements):
        self.elements = elements

class Var:
    def __init__(self, name):
        self.name = name

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Print:
    def __init__(self, exprs, sep=None):
        self.exprs = exprs
        self.sep = sep

class Assign:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class If:
    def __init__(self, cond, body, else_body=None):
        self.cond = cond
        self.body = body
        self.else_body = else_body

class ForEach:
    def __init__(self, var, iterable, body):
        self.var = var
        self.iterable = iterable
        self.body = body

class FuncDef:
    def __init__(self, name, params, body, defaults=None, variadic=None):
        self.name = name
        self.params = params
        self.body = body
        self.defaults = defaults or {}
        self.variadic = variadic

class Call:
    def __init__(self, callee, args):
        self.callee = callee
        self.args = args
