# Changelog

All notable changes to BolBachan are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] — 2025

### First public release — Course project → Open source

**Added**
- Complete Hinglish keyword set: `rakho`, `bolBhai`, `agar`/`toh`/`nahiToh`, `jabTak`, `baarBaar`, `jodo`/`ghatao`/`guna`/`bhaag`, `badaHai`/`chhotaHai`/`barabarHai`, `wapis`, `function`
- `naBrabar` operator for not-equal (`!=`)
- `sahi` and `galat` as Hindi aliases for `true` and `false`
- Logical NOT operator `!`
- `if` without `else` (`agar...toh` without `nahiToh`)
- Float literal support (`3.14`, `0.5`)
- String concatenation via `jodo` (same operator as numeric add)
- `//` line comments (discarded by lexer)
- Proper operator precedence (`guna`/`bhaag` before `jodo`/`ghatao`)
- Division by zero raises `DivisionByZero` with a helpful message (in Hindi!)
- Undefined variable access raises `UndefinedVariable` with suggestion
- Wrong argument count raises `ArityError`
- Undefined function call raises `UndefinedFunction`
- Interactive REPL with `.ast`, `.reset`, `.help` meta-commands and `chhodo` to quit
- CLI flags: `--ast`, `--parse-only`, `--version`
- Public library API in `src/bolbachan/__init__.py`: `run_file()`, `run_string()`, `parse()`
- Package structure: `src/bolbachan/` with `lexer.py`, `parser.py`, `interpreter.py`, `errors.py`
- `pytest` test suite covering lexer tokens, interpreter semantics, error handling
- 7 example programs: `hello_world`, `arithmetic`, `conditions`, `loops`, `functions`, `fibonacci`, `fizzbuzz`
- EBNF formal grammar specification in `docs/grammar.md`
- Complete language reference in `docs/language-reference.md`
- MIT License
- CONTRIBUTING.md guide for contributors
- ROADMAP.md with short/medium/long-term plans

**Fixed**
- Double-parse bug: source was parsed twice (once for tree print, once for execution); now parsed once
- `from parser import parser` name collision with Python stdlib `parser` module; resolved via package structure
- Spurious `INVALID_ID` errors for identifiers like `for`, `print`, `if` — English reserved words were wrongly included in BolBachan's reserved set
- No operator precedence: `1 jodo 2 guna 3` now correctly evaluates to `7`, not `9`
- Dead grammar rules `p_for_init` and `p_declaration` removed
- `None` returned silently for undefined variables; now raises `UndefinedVariable`
- `ZeroDivisionError` from Python leaked through; now caught and re-raised as `DivisionByZero`
- Boolean values printed as Python `True`/`False`; now printed as `sahi`/`galat`
- `None` printed as `None`; now printed as `khaali`

**Changed**
- Canonical project name standardised to **BolBachan** (not "BolBachchan")
- `src/main.py` moved to project root `main.py`
- Core language code moved to `src/bolbachan/` package
- `data/` samples preserved; new improved examples added to `examples/`

---

## [0.1.0] — 2025 (Course submission — Team 32, SER502)

Initial implementation for Arizona State University Programming Paradigms course.

- Lexer with PLY (`src/lexer.py`)
- Parser with PLY YACC (`src/parser.py`)
- Tree-walking interpreter (`src/interpreter.py`)
- Basic variables, arithmetic, if-else, while, for, functions
- 5 sample programs in `data/`
- PDF grammar specification and course presentation in `doc/`
