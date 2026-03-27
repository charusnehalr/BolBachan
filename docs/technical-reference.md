# BolBachan — Technical Reference

Full technical documentation for the BolBachan language and interpreter.

---

## Language at a Glance

| Feature | BolBachan Syntax | Equivalent |
|---------|-----------------|---------|
| Assign | `rakho x = 5;` | `x = 5` |
| Print | `bolBhai(x);` | `print(x)` |
| If-else | `agar (c) toh {...} nahiToh {...}` | `if c: ... else: ...` |
| While | `jabTak (c) {...}` | `while c: ...` |
| For | `baarBaar (rakho i=0; i chhotaHai 5; i=i jodo 1) {...}` | `for i in range(5):` |
| Function | `function add(a, b) { wapis a jodo b; }` | `def add(a,b): return a+b` |
| Add | `a jodo b` | `a + b` |
| Subtract | `a ghatao b` | `a - b` |
| Multiply | `a guna b` | `a * b` |
| Divide | `a bhaag b` | `a // b` |
| Greater | `a badaHai b` | `a > b` |
| Less | `a chhotaHai b` | `a < b` |
| Equal | `a barabarHai b` | `a == b` |
| Not Equal | `a naBrabar b` | `a != b` |
| AND | `a & b` | `a and b` |
| OR | `a \| b` | `a or b` |
| NOT | `!a` | `not a` |
| Ternary | `cond ? x : y` | `x if cond else y` |
| String join | `"Hi " jodo name` | `"Hi " + name` |
| Comment | `// text` | `# text` |

---

## Keyword Dictionary

| Hinglish | Meaning |
|----------|---------|
| `rakho` | keep / assign |
| `bolBhai` | say, brother / print |
| `agar` | if |
| `toh` | then |
| `nahiToh` | otherwise / else |
| `jabTak` | as long as / while |
| `baarBaar` | again and again / for |
| `jodo` | add / join |
| `ghatao` | subtract |
| `guna` | multiply |
| `bhaag` | divide |
| `badaHai` | is greater than |
| `chhotaHai` | is less than |
| `barabarHai` | is equal to |
| `naBrabar` | is not equal to |
| `wapis` | back / return |
| `sahi` | correct / true |
| `galat` | wrong / false |
| `khaali` | empty / null |

---

## Project Structure

```
BolBachan/
├── main.py                    ← CLI entry point + REPL
├── app.py                     ← Streamlit web playground
├── src/
│   └── bolbachan/
│       ├── __init__.py        ← Public API: run_file(), run_string(), parse()
│       ├── lexer.py           ← PLY lexer — tokenizes .bb source
│       ├── parser.py          ← PLY parser — builds AST from token stream
│       ├── interpreter.py     ← Tree-walking interpreter — evaluates AST
│       └── errors.py          ← Exception hierarchy
├── examples/                  ← Ready-to-run .bb programs
├── tests/                     ← pytest test suite (91 tests)
│   ├── conftest.py
│   ├── test_lexer.py
│   └── test_interpreter.py
├── docs/
│   ├── grammar.md             ← Formal EBNF grammar specification
│   ├── language-reference.md  ← Complete language reference
│   └── technical-reference.md ← This file
├── data/                      ← Original course submission samples
├── doc/                       ← Original course PDFs
├── requirements.txt
├── CONTRIBUTING.md
├── ROADMAP.md
└── CHANGELOG.md
```

---

## Architecture

```
Source (.bb file)
       │
       ▼
  ┌──────────┐  token stream  ┌──────────┐  AST tuples  ┌───────────────┐
  │  Lexer   │ ─────────────▶ │  Parser  │ ────────────▶ │  Interpreter  │
  │ lexer.py │                │ parser.py│               │interpreter.py │
  └──────────┘                └──────────┘               └───────────────┘
    PLY lex                   PLY yacc / LALR(1)           Tree-walker
```

### AST Node Format

All AST nodes are plain Python tuples: `('node_type', child1, child2, ...)`

```python
# Source:  rakho x = 3 jodo 4;
# AST:
('program', [
    ('assign', 'x',
        ('binary_op', 'jodo',
            ('number', 3),
            ('number', 4)))
])
```

Full node reference:

| Node | Shape |
|------|-------|
| `program` | `('program', [stmt, ...])` |
| `assign` | `('assign', name, expr)` |
| `declare` | `('declare', type, name)` |
| `print` | `('print', expr)` |
| `if_else` | `('if_else', cond, then_block, else_block)` |
| `if` | `('if', cond, then_block)` |
| `while` | `('while', cond, body)` |
| `for` | `('for', init, cond, post, body)` |
| `function_def` | `('function_def', name, [params], body)` |
| `function_call` | `('function_call', name, [args])` |
| `return` | `('return', expr)` |
| `binary_op` | `('binary_op', op_kw, left, right)` |
| `relational_op` | `('relational_op', op_kw, left, right)` |
| `logical_op` | `('logical_op', symbol, left, right)` |
| `ternary` | `('ternary', cond, true_expr, false_expr)` |
| `var` | `('var', name)` |
| `number` | `('number', int_value)` |
| `float` | `('float', float_value)` |
| `string` | `('string', str_value)` |
| `bool` | `('bool', bool_value)` |

---

## CLI Reference

```bash
python main.py                        # Start interactive REPL
python main.py <file.bb>              # Run a file
python main.py <file.bb> --ast        # Print AST, then run
python main.py <file.bb> --parse-only # Parse only, do not execute
python main.py --version              # Print version
```

---

## Interactive REPL

```
$ python main.py

  +========================================+
  |  BolBachan v1.0.0 -- Hinglish REPL     |
  |  Type 'chhodo' or Ctrl-D to exit      |
  +========================================+

bolbachan> rakho x = 42;
bolbachan> bolBhai("Answer: " jodo x);
Answer: 42
bolbachan> .ast
AST display ON
bolbachan> rakho y = 2 jodo 3;
-- AST --
(program ...)
---------
bolbachan> chhodo
Alvida!
```

**REPL meta-commands:**

| Command | Effect |
|---------|--------|
| `chhodo` | quit |
| `.ast` | toggle AST display on/off |
| `.reset` | clear all variables and functions |
| `.help` | show help |

---

## Using as a Python Library

```python
import sys
sys.path.insert(0, "src")

from bolbachan import run_file, run_string, parse

# Run a .bb file
run_file("examples/hello_world.bb")

# Run source code from a string
run_string('bolBhai("Namaste!");')

# Get just the AST (no execution)
ast = parse("rakho x = 1 jodo 2;")
print(ast)
# ('program', [('assign', 'x', ('binary_op', 'jodo', ('number', 1), ('number', 2)))])
```

---

## Error Reference

| Error class | When it's raised |
|-------------|-----------------|
| `LexError` | Unrecognized character in source |
| `ParseError` | Invalid syntax |
| `UndefinedVariable` | Variable used before `rakho` |
| `UndefinedFunction` | Function called before `function` definition |
| `ArityError` | Wrong number of arguments in function call |
| `DivisionByZero` | `bhaag` by zero |
| `BolBachanError` | Base class for all of the above |

---

## Running Tests

```bash
pip install pytest
pytest tests/ -v          # run all 91 tests
pytest tests/test_lexer.py -v
pytest tests/test_interpreter.py -v
```

---

## Scoping Rules

- `rakho x = val` at top level → global scope
- `rakho x = val` inside a loop or if/else → **same** scope as the enclosing block (no new scope boundary)
- `rakho x = val` inside a function → local to that function call; cannot mutate globals
- Functions can **read** global variables but **not modify** them
- Functions are **hoisted** — you can call a function defined later in the file

---

## Operator Precedence (high → low)

| Level | Operator | Description |
|-------|----------|-------------|
| 6 | `( expr )` | Grouping |
| 5 | `guna`, `bhaag` | Multiply, divide |
| 4 | `jodo`, `ghatao` | Add, subtract |
| 3 | `badaHai`, `chhotaHai`, `barabarHai`, `naBrabar` | Relational |
| 2 | `!` | Logical NOT |
| 1 | `&` | Logical AND |
| 0 | `\|` | Logical OR |
| -1 | `? :` | Ternary (right-associative) |

See [grammar.md](grammar.md) for the full EBNF specification.
