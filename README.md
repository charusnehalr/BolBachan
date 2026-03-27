# BolBachan 🎬

> **A Hinglish programming language — where code speaks your language.**

BolBachan is a custom interpreted programming language that blends Hindi and English keywords into a fun, expressive syntax. Built entirely in Python with PLY, it features a handwritten lexer, parser, AST, and tree-walking interpreter. Designed for a Programming Paradigms course, it demonstrates core concepts of language design: lexical analysis, grammar specification, AST construction, and runtime evaluation.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![PLY](https://img.shields.io/badge/PLY-3.11-green.svg)](https://github.com/dabeaz/ply)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What makes BolBachan unique?

- **Hinglish keywords** — `rakho` (assign), `bolBhai` (print), `agar` (if), `jodo` (add), `wapis` (return)
- **Full interpreter pipeline** — lexer → parser → AST → tree-walker, all from scratch
- **Formally specified grammar** — EBNF grammar document included
- **Imperative + Procedural** — variables, loops, conditionals, user-defined functions, recursion
- **Interactive REPL** — live code execution with `.ast` toggle and state reset
- **Helpful errors** — clear error messages with line numbers and suggestions
- **Zero extra dependencies** — just Python 3.8+ and one library (PLY)

---

## Quick Start

```bash
# 1. Clone and install
git clone https://github.com/YOUR_USERNAME/BolBachan.git
cd BolBachan
pip install -r requirements.txt

# 2. Run a program
python main.py examples/hello_world.bb

# 3. Start the interactive REPL
python main.py

# 4. Show the AST for a program
python main.py examples/fibonacci.bb --ast
```

---

## Your First BolBachan Program

```
// hello.bb
rakho name = "Duniya";
bolBhai("Namaste, " jodo name jodo "!");

baarBaar (rakho i = 1; i chhotaHai 6; i = i jodo 1) {
    bolBhai("Counting: " jodo i);
}

function greet(who) {
    wapis "BolBachan kehta hai: Namaste, " jodo who jodo "!";
}

bolBhai(greet("World"));
```

Output:
```
Namaste, Duniya!
Counting: 1
Counting: 2
Counting: 3
Counting: 4
Counting: 5
BolBachan kehta hai: Namaste, World!
```

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

## Examples

The `examples/` directory contains ready-to-run programs:

| File | What it shows |
|------|--------------|
| `hello_world.bb` | Basic output |
| `arithmetic.bb` | All math operators + string concatenation |
| `conditions.bb` | if/else, ternary, logical operators |
| `loops.bb` | for and while loops |
| `functions.bb` | User-defined functions + recursion |
| `fibonacci.bb` | Fibonacci via recursion and iteration |
| `fizzbuzz.bb` | Classic FizzBuzz problem |

---

## Project Structure

```
BolBachan/
├── main.py                    ← CLI entry point + REPL
├── src/
│   └── bolbachan/
│       ├── __init__.py        ← Public API: run_file(), run_string(), parse()
│       ├── lexer.py           ← PLY lexer — tokenizes .bb source
│       ├── parser.py          ← PLY parser — builds AST from token stream
│       ├── interpreter.py     ← Tree-walking interpreter — evaluates AST
│       └── errors.py          ← Exception hierarchy
├── examples/                  ← Ready-to-run .bb programs
├── tests/                     ← pytest test suite
│   ├── test_lexer.py
│   └── test_interpreter.py
├── docs/
│   ├── grammar.md             ← Formal EBNF grammar specification
│   └── language-reference.md ← Complete language reference
├── data/                      ← Original sample programs (course submission)
├── doc/                       ← Original course documentation & grammar PDF
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
    PLY lex                   PLY yacc                     Tree-walker
```

AST nodes are plain Python tuples. Example:

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

---

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

---

## Interactive REPL

```
$ python main.py

  ╔══════════════════════════════════════╗
  ║   BolBachan v1.0.0 — Hinglish REPL  ║
  ║   Type 'chhodo' or Ctrl-D to exit   ║
  ╚══════════════════════════════════════╝

bolbachan> rakho x = 42;
bolbachan> bolBhai("Answer: " jodo x);
Answer: 42
bolbachan> .ast
AST display ON
bolbachan> rakho y = 2 jodo 3;
── AST ──
(program
  (assign
    'y'
    (binary_op
      'jodo'
      (number
        2)
      (number
        3))))
─────────
bolbachan> chhodo
Alvida!
```

---

## CLI Reference

```
python main.py                        # Start REPL
python main.py <file.bb>              # Run a file
python main.py <file.bb> --ast        # Print AST, then run
python main.py <file.bb> --parse-only # Parse only, no execution
python main.py --version              # Print version
```

---

## Using as a Library

```python
import sys
sys.path.insert(0, "src")

from bolbachan import run_file, run_string, parse

run_file("examples/hello_world.bb")        # run a file
run_string('bolBhai("Namaste!");')          # run a string
ast = parse("rakho x = 1 jodo 2;")         # get AST
```

---

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the full plan.

**Next up:** modulo operator · `else-if` chains · string escape sequences · web playground

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). PRs, bug reports, and language design suggestions are all welcome.

---

## Team

Created by **Team 32** for **SER502 — Programming Paradigms** at Arizona State University.

| Member | Contribution |
|--------|-------------|
| Aditya Soude | Parser design & implementation |
| Savankumar Pethani | Grammar design |
| Vidhisha Amle | Lexer implementation |
| Charu Sneha | Interpreter, testing, integration |

---

## License

[MIT](LICENSE) — free to use, modify, and distribute.

---

📺 [Demo Video](https://youtu.be/Eu3Vn_AxoQg) · 📖 [Language Reference](docs/language-reference.md) · 📐 [Grammar Spec](docs/grammar.md)
