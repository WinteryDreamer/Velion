
# Velion Lang

Velion is a minimalist and didactic programming language, inspired by pseudocode, with ultra-simple, self-explanatory English-like syntax.

## Installation

Clone this repository and run:

```bash
python -m velion <file.vl>
```

If you are using the .exe version of Velion, just use:
```bash
velion <file.vl>
```

## Project Structure

- `velion/` — Interpreter implementation:
  - `lexer.py` — Lexical analyzer (tokenizer)
  - `ast_nodes.py` — AST class definitions
  - `parser.py` — Syntax analyzer (parser)
  - `runtime.py` — AST execution (runtime)
  - `__main__.py` — Interpreter entry point
  - `__init__.py` — Makes the directory a Python package
- `examples/` — Example `.vl` files
- `docs/FEATURES.md` — Detailed documentation of language features

## Supported Features

See the full list of commands, operators, and examples in [`docs/FEATURES.md`](docs/FEATURES.md).

### Main commands and structures:

- **say <expr>** — prints values
- **remember <expr> as <name>** — variable assignment
- **if ... is ... then ... else ... end** — conditionals
- **for each ... in ... do ... end** — loop
- **when name(param, ...)** — function definition
- **Function call** — `name(arg1, arg2)`

### Data types:
- Integers and floats
- Strings
- Lists
- Dictionaries: `{key: value}`
- Booleans: `yes` (True), `no` (False)

### Operators:
- Arithmetic: `+`, `-`, `*`, `/`
- Concatenation: `..` (for strings)
- Comparison: `==`, `!=`, `>`, `<`, `>=`, `<=`
- Logical: `and`, `or`, `not`

### Built-in functions:
- `length(list or text)` — length of a list or string
- `to_number(value)` — convert to number
- `to_string(value)` — convert to string

### Anonymous functions (lambda):
- Define inline functions with `do (x, y) -> ... end` or `lambda (x, y) -> ... end`.
- Example:
  ```velion
  remember do (x) -> x * 2 end as double
  say double(5)
  ```

### Native modules and utilities:
- `min`, `max`, `sort`, `reverse`, `exit`, `wait`, `clear`.
- Example: `say min(1, 2, 3)`

### Embedded documentation:
- Use `doc "description" when ...` to document functions.

### Advanced and ultra-simple features (already available!):
- **String interpolation:** `say "Hello, {name}!"`
- **Optional and variadic arguments:** `when greet(name, greeting = "Hi")`, `when sum(...)`
- **Natural formatted output:** `say "a", "b", "c" with ", " between`
- **Dictionary iteration:** `for each key, value in dict do ... end`
- **Natural assignment:** `add 1 to x`, `subtract 2 from x`, `multiply x by 3`, `divide x by 2`

### Error handling:
- Block `try ... if_it_fails ... end` for simple error capture.
- Example:
  ```velion
  try
    remember 10 / 0 as x
  if_it_fails
    say "Division error!"
  end
  ```

## Notes

- Local variables in functions do not affect the global scope
- Functions can return values with `return`
- User input available with `input`
- Explicit booleans: `yes` (True), `no` (False)
- Dictionaries and lists can be nested

## License

MIT
