from .lexer import lex
from .parser import Parser
from .runtime import run

def run_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        code = f.read()
    tokens = lex(code)
    parser = Parser(tokens)
    stmts = parser.parse()
    run(stmts)

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: velion <file.vl>")
        return
    run_file(sys.argv[1])

if __name__ == "__main__":
    main()
