# Features (seriously, just use your logic and you will be able to code)

## String Interpolation

- Use curly braces to insert variables directly into text:
  ```velion
  remember "Ana" as name
  say "Hello, {name}!"
  ```

## Formatted output and multiple values

- Print several values at once, separated by any text, in a natural way:
  ```velion
  say "a", "b", "c" with ", " between
  say 1, 2, 3 with " - " between
  ```

## Optional and Variadic Function Arguments

- Functions can have default values and receive any number of arguments:
  ```velion
  when greet(name, greeting = "Hi")
      say greeting, name
  end
  greet("Ana") # Hi Ana
  greet("Ana", "Hello") # Hello Ana

  when sum(...)
      remember 0 as total
      for each item in args do
          add item to total
      end
      say total
  end
  sum(1,2,3,4) # 10
  ```

## Dictionary Iteration

- Easily loop through keys and values of a dictionary:
  ```velion
  remember {"name": "Ana", "age": 20} as person
  for each key, value in person do
      say key, value with ": " between
  end
  ```

## Natural Assignment (no symbols)

- Update variables using logic and plain English:
  ```velion
  remember 10 as x
  add 5 to x
  say x # 15
  subtract 2 from x
  say x # 13
  multiply x by 2
  say x # 26
  divide x by 2
  say x # 13
  ```

# Velion Language Supported Features

## Commands and Structures

- **say <expr>**
  - Prints the value of an expression.
  - Example: `say "Hello"`, `say x + 1`

- **remember <expr> as <name>**
  - Assigns the value of an expression to a variable.
  - Example: `remember 10 as x`

- **if <condition> then ... else ... end**
  - Conditional structure.
  - Supports operators: `is greater than`, `is less than`, `is equal to`, `is not equal to`, `is greater than or equal to`, `is less than or equal to`, `is not greater than`, `is not less than`.
  - Example:
    ```velion
    if x is greater than 5 then
        say "greater"
    else
        say "less or equal"
    end
    ```

- **for each <var> in <list> do ... end**
  - Loop to iterate over lists.
  - Example:
    ```velion
    remember [1,2,3] as list
    for each item in list do
        say item
    end
    ```

- **when <name>(<params>) ... end**
  - Function definition.
  - Exemplo:
    ```velion
    when sum(a, b)
        say a + b
    end
    sum(2, 3)
    ```

- **Function call**
  - Example: `sum(1, 2)`

- **input <expr>**
  - Reads user input and stores in `_last_input`.
  - Example: `input "Type something: "`

- **return <expr>**
  - Returns a value from a function.
  - Example:
    ```velion
    when sum(a, b)
        return a + b
    end
    say sum(2, 3)
    ```

## Data Types

- **Integers and floats**: `10`, `3.14`
- **Strings**: `"text"`
- **Lists**: `[1, 2, 3]`, `["a", "b"]`
- **Booleans**: `yes` (true), `no` (false)
- **Dictionaries**: `{key: value, ...}`
  - Example: `remember {"name": "Ana", "age": 20} as person`

## Operators

- **Arithmetic**: `+`, `-`, `*`, `/`
- **Concatenation**: `..` (for strings)
- **Comparison**: `==`, `!=`, `>`, `<`, `>=`, `<=`
- **Logical operators**: `and`, `or`, `not`
  - Example: `if x is greater than 5 and y is less than 10 then ... end`

## Built-in Functions

- `length(list)` — returns the length of a list or string
- `to_number(value)` — converts to number
- `to_string(value)` — converts to string

## Notes
- Variables are global (except function parameters)
- Functions can return values (with `return`)
- User input is available (with `input`)
- Explicit booleans: `yes` (true), `no` (false)
- **# comment**
  - Any line starting with `#` is ignored.

- **File import:**
  - **get <file>**
    - Imports and executes another `.vl` file in the same environment.
    - Example: `get "util.vl"`
