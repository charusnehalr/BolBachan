# BolBachan 🎬

> A programming language that speaks Hinglish — because why should code only speak English?

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![PLY](https://img.shields.io/badge/PLY-3.11-green.svg)](https://github.com/dabeaz/ply)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![SER502](https://img.shields.io/badge/ASU-SER502%20Project-8C1D40.svg)](https://engineering.asu.edu)

---

## What it does

BolBachan is a fully interpreted programming language built from scratch for **SER502 — Programming Paradigms at Arizona State University**. It uses **Hinglish keywords** (Hindi + English) so that code reads more like how South Asian developers naturally think and speak. You write `rakho x = 5` instead of `let x = 5`, `bolBhai(x)` instead of `print(x)`, and `agar` / `nahiToh` instead of `if` / `else`.

Under the hood it implements a complete language pipeline: **lexer → parser → AST → tree-walking interpreter**, all written in Python without any language framework shortcuts.

---

## Tech Stack

- **Python 3.8+** — interpreter runtime
- **PLY (Python Lex-Yacc)** — lexer and LALR(1) parser
- **Streamlit** — interactive web playground
- **pytest** — test suite (91 tests)

---

## Features

- **Hinglish syntax** — `rakho`, `bolBhai`, `agar`, `jodo`, `wapis` and more
- **Full interpreter pipeline** — lexer, parser, AST, and tree-walker built from scratch
- **Variables & types** — int, float, string, bool (`sahi`/`galat`)
- **Arithmetic** — `jodo` (+), `ghatao` (−), `guna` (×), `bhaag` (÷) with correct precedence
- **Conditionals** — `agar/toh/nahiToh` (if/then/else) + ternary `? :`
- **Loops** — `baarBaar` (for) and `jabTak` (while)
- **Functions** — user-defined with parameters, return via `wapis`, full recursion
- **String concatenation** — same `jodo` operator works for strings too
- **Comments** — `//` line comments
- **Interactive REPL** — live code execution in the terminal
- **Web Playground** — browser UI with examples, output panel, and AST viewer
- **Helpful errors** — clear messages with suggestions when things go wrong
- **Formal grammar** — EBNF specification documented in `docs/grammar.md`

---

## Demo / Screenshots

> **Web Playground**

<img width="1837" height="907" alt="image" src="https://github.com/user-attachments/assets/2099c10c-5387-4a80-abb8-827c694c2a64" />

<img width="1831" height="909" alt="image" src="https://github.com/user-attachments/assets/26c47f80-1fda-4517-84c6-1586c7287c9c" />

<img width="1840" height="902" alt="image" src="https://github.com/user-attachments/assets/4c61ae45-c61d-487f-a042-9fcca132f0cb" />

<img width="1815" height="853" alt="image" src="https://github.com/user-attachments/assets/cbdc707b-73ed-45f8-8568-f1d1f2632f4f" />

---

## How to Run

**Clone and install:**
```bash
git clone https://github.com/YOUR_USERNAME/BolBachan.git
cd BolBachan
pip install -r requirements.txt
```

**Run a program:**
```bash
python main.py examples/hello_world.bb
python main.py examples/fibonacci.bb
python main.py examples/fizzbuzz.bb
```

**Start the web playground:**
```bash
streamlit run app.py
# Open http://localhost:8501
```

**Start the interactive REPL:**
```bash
python main.py
```

**Run the test suite:**
```bash
pip install pytest
pytest tests/ -v      # 91 tests
```

**Other CLI options:**
```bash
python main.py program.bb --ast        # show parse tree
python main.py program.bb --parse-only # parse without running
python main.py --version
```

---

## Write Your First BolBachan Program

```
// hello.bb

rakho name = "Duniya";
bolBhai("Namaste, " jodo name jodo "!");

function factorial(n) {
    agar (n chhotaHai 2) toh {
        wapis 1;
    }
    wapis n guna factorial(n ghatao 1);
}

bolBhai("5! = " jodo factorial(5));
```

Output:
```
Namaste, Duniya!
5! = 120
```

---

## Keyword Reference

| BolBachan | Meaning | English equivalent |
|-----------|---------|-------------------|
| `rakho` | keep / store | `let` / `=` |
| `bolBhai` | say, brother! | `print()` |
| `agar` / `toh` | if / then | `if` |
| `nahiToh` | otherwise | `else` |
| `jabTak` | as long as | `while` |
| `baarBaar` | again and again | `for` |
| `jodo` | add / join | `+` |
| `ghatao` | subtract | `-` |
| `guna` | multiply | `*` |
| `bhaag` | divide | `//` |
| `badaHai` | is greater than | `>` |
| `chhotaHai` | is less than | `<` |
| `barabarHai` | is equal to | `==` |
| `naBrabar` | is not equal to | `!=` |
| `wapis` | go back / return | `return` |
| `sahi` / `galat` | correct / wrong | `true` / `false` |

---

## Architecture

```
Source (.bb)
    │
    ▼
[ Lexer ]  ──token stream──▶  [ Parser ]  ──AST tuples──▶  [ Interpreter ]
 lexer.py                      parser.py                    interpreter.py
 PLY lex                       PLY yacc / LALR(1)           Tree-walker
```

AST nodes are plain Python tuples — simple, inspectable, no magic:
```python
# rakho x = 3 jodo 4;
('program', [
    ('assign', 'x',
        ('binary_op', 'jodo', ('number', 3), ('number', 4)))
])
```

**Project structure:**
```
BolBachan/
├── main.py              ← CLI + REPL
├── app.py               ← Streamlit web playground
├── src/bolbachan/
│   ├── lexer.py         ← Tokenizer
│   ├── parser.py        ← Grammar + AST builder
│   ├── interpreter.py   ← Tree-walking evaluator
│   └── errors.py        ← Error hierarchy
├── examples/            ← 7 sample programs
├── tests/               ← 91 pytest tests
└── docs/                ← Grammar spec + language reference
```

---

## Why We Built This

This started as a simple question our team had during SER502: **what if a programming language used the way bilingual people actually think?**

Most developers who grew up speaking Hindi, Urdu, or other South Asian languages mentally translate between their native language and English while coding. We wanted to see what it felt like to remove that translation step — not by replacing English entirely, but by blending the two the way people naturally speak: Hinglish.

**The tradeoffs we made:**

- We chose a **tree-walking interpreter** over bytecode compilation — it is slower but the AST stays visible and inspectable, which is better for a teaching language where understanding the execution model matters.
- We used **PLY (Python Lex-Yacc)** over writing a hand-rolled parser — this let us define the grammar formally in EBNF style and forced us to think carefully about operator precedence, shift/reduce conflicts, and ambiguity.
- `jodo` (add) **doubles as string concatenation** — same operator, different behavior based on types. This was a deliberate design choice to keep the keyword count low and let the language feel lightweight.
- We chose **keyword-based operators** (`jodo`, `ghatao`) over symbols (`+`, `-`) for arithmetic — this makes the language feel distinctly non-English even though the structure is familiar.

**What we learned:**

Building a language from scratch — even a simple one — forces you to make decisions that textbooks hand you for free. Operator precedence, scope rules, function hoisting, how errors surface to the user — every one of these required a concrete choice and exposed us to exactly the tradeoffs real language designers face.

---

## Team — SER502 Group 32, ASU

| Member | Role |
|--------|------|
| Aditya Soude | Parser design & implementation |
| Savankumar Pethani | Grammar design |
| Vidhisha Amle | Lexer implementation |
| Charu Sneha | Interpreter, testing, integration |

---

## License

[MIT](LICENSE) — free to use, learn from, and build on.

---

[Demo Video](https://youtu.be/Eu3Vn_AxoQg) · [Language Reference](docs/language-reference.md) · [Grammar Spec](docs/grammar.md) ·[Examples](examples/)
