# BolBachan Roadmap

This document tracks planned improvements to the language, interpreter, tooling, and ecosystem.

---

## v1.0 — Current (Course Submission → Open Source)

**Completed:**
- [x] Lexer with full Hinglish keyword set
- [x] PLY-based parser with proper operator precedence
- [x] Tree-walking interpreter
- [x] Variables, arithmetic, relational, logical operators
- [x] if/else conditionals + ternary operator
- [x] for and while loops
- [x] User-defined functions with parameters
- [x] Recursion
- [x] String concatenation via `jodo`
- [x] Float literals
- [x] `//` line comments
- [x] `if` without else
- [x] `naBrabar` (!=) operator
- [x] `sahi`/`galat` as Hindi aliases for true/false
- [x] Logical NOT `!`
- [x] Clear error hierarchy with helpful messages
- [x] Interactive REPL with `.ast` toggle
- [x] CLI with `--ast`, `--parse-only`, `--version` flags
- [x] Public library API (`run_file`, `run_string`, `parse`)
- [x] `pytest` test suite (lexer + interpreter)
- [x] EBNF grammar specification
- [x] Language reference documentation
- [x] MIT License

---

## v1.1 — Short Term

**Language:**
- [ ] Modulo operator — `shakesh` or `baaki` (remainder)
- [ ] `else-if` chains — `nahiToh agar` shorthand
- [ ] String escape sequences — `\n`, `\t`, `\\`, `\"`
- [ ] Negative number literals — `-5` instead of `0 ghatao 5`
- [ ] Float division — when either operand is a float, produce float result
- [ ] Comparison chaining — `1 chhotaHai x chhotaHai 10`

**Tooling:**
- [ ] `--no-hoist` flag to disable function hoisting (for pedagogical demos)
- [ ] Line-level error messages in all error types
- [ ] REPL history (using `readline` on Unix)
- [ ] `.bolbachan` as alternative file extension

**Tests:**
- [ ] Parser-level tests
- [ ] End-to-end integration tests for all example programs
- [ ] Edge case tests (empty programs, deeply nested functions, etc.)

---

## v1.2 — Medium Term

**Language:**
- [ ] Arrays / lists — `suchi` type
  ```
  rakho nums = [1, 2, 3, 4, 5];
  bolBhai(nums[0]);
  ```
- [ ] String indexing — `text[0]`
- [ ] `len` built-in function
- [ ] `mod` built-in (or as an operator)
- [ ] `input` built-in — read from stdin
  ```
  rakho name = sun();     // "sun" = listen
  ```
- [ ] Multi-line strings

**Tooling:**
- [ ] Syntax highlighting — VS Code extension (TextMate grammar)
- [ ] `bolbachan` executable script (via `pip install`)
- [ ] `--format` flag to pretty-print/reformat BolBachan source

---

## v1.3 — Web Playground

**Full-stack web application:**
- [ ] Browser-based code editor (Monaco Editor)
- [ ] Real-time execution via REST API backend
- [ ] AST visualizer — expandable tree view
- [ ] Built-in examples browser (one-click load)
- [ ] Shareable code links (URL-encoded source)
- [ ] Error highlighting in editor

**Architecture:**
- Frontend: React + Monaco Editor + Tailwind CSS
- Backend: FastAPI + sandboxed subprocess execution
- Hosting: Vercel (frontend) + Railway or Render (backend)

---

## v2.0 — Language Maturity

**Language:**
- [ ] Dictionaries / maps — `theli` type
  ```
  rakho person = {naam: "Arjun", age: 25};
  bolBhai(person["naam"]);
  ```
- [ ] Higher-order functions — pass functions as arguments
- [ ] Anonymous functions / lambdas
  ```
  rakho square = kaam(n) { wapis n guna n; };
  ```
- [ ] `foreach` loop — `harEk`
  ```
  harEk (item, nums) { bolBhai(item); }
  ```
- [ ] Type annotations with enforcement
- [ ] Module system — `leao "math"` (import)
- [ ] Standard library:
  - Math: `abs`, `max`, `min`, `pow`, `sqrt`
  - String: `length`, `upper`, `lower`, `trim`
  - Type conversion: `toInt`, `toString`

**Tooling:**
- [ ] Bytecode compiler + VM (performance improvement)
- [ ] Debugger with step-through and variable inspection
- [ ] Language Server Protocol (LSP) for IDE support
- [ ] Package manager for BolBachan libraries

---

## Stretch Goals

- [ ] Compile to WebAssembly for in-browser execution
- [ ] Transpile to Python for interop
- [ ] Interactive tutorial website with exercises
- [ ] BolBachan playground as an embeddable widget
- [ ] Discord bot that executes BolBachan snippets
- [ ] Object-oriented extension with `varg` (class)

---

## Contributing

Have an idea? Open an issue to discuss it before implementing. See [CONTRIBUTING.md](CONTRIBUTING.md).
