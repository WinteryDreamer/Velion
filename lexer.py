import re

TOKEN_SPEC = [
    ('NUMBER',   r'\d+(\.\d+)?'),
    ('STRING',   r'"([^"\\]|\\.)*"'),
    ('COMMENT',  r'#.*'),
    ('KEYWORD',  r'\b(say|input|remember|if|then|end|for|each|in|do|when|else|as|is|greater|less|than|not|and|or|yes|no|return|length|to_number|to_string|get|try|if_it_fails|lambda|exit|wait|clear|min|max|sort|reverse|doc)\b'),
    ('IDENT',    r'[A-Za-z_][A-Za-z0-9_]*'),
    ('COMPARE',  r'==|!=|<=|>=|<|>'),
    ('CONCAT',   r'\.\.'),
    ('PLUS',     r'\+'),
    ('MINUS',    r'-'),
    ('MULT',     r'\*'),
    ('DIV',      r'/'),
    ('LBRACE',   r'\{'),
    ('RBRACE',   r'\}'),
    ('COLON',    r':'),
    ('PUNCT',    r'[\(\),\[\]]'),
    ('SKIP',     r'[ \t]+'),
    ('NEWLINE',  r'\n'),
    ('MISMATCH', r'.'),
]

token_re = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC))

def lex(code):
    pos = 0
    tokens = []
    while pos < len(code):
        m = token_re.match(code, pos)
        if not m:
            raise SyntaxError(f"Unexpected character at position {pos}")
        kind = m.lastgroup
        value = m.group()
        pos = m.end()
        if kind in ('SKIP', 'NEWLINE'):
            continue
        if kind == 'STRING':
            value = value[1:-1]
        tokens.append((kind, value))
    tokens.append(('EOF', ''))
    return tokens
