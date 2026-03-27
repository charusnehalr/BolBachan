# Contributing to BolBachan

Thank you for wanting to help BolBachan grow! Whether you are fixing a bug, proposing a new language feature, improving documentation, or adding an example program — contributions of all sizes are welcome.

---

## Table of Contents

1. [Ways to Contribute](#ways-to-contribute)
2. [Getting Started](#getting-started)
3. [Project Structure](#project-structure)
4. [Making a Change](#making-a-change)
5. [Adding a Language Feature](#adding-a-language-feature)
6. [Writing Tests](#writing-tests)
7. [Code Style](#code-style)
8. [Submitting a Pull Request](#submitting-a-pull-request)

---

## Ways to Contribute

- **Bug reports** — open an issue with a minimal reproducible example
- **Feature requests** — open an issue describing the feature and why it fits BolBachan
- **Language features** — implement new syntax in the lexer/parser/interpreter
- **Example programs** — add new `.bb` programs to `examples/`
- **Documentation** — improve the language reference or grammar spec
- **Tests** — expand the test suite coverage
- **Web playground** — frontend/backend for a browser-based code editor

---

## Getting Started

```bash
git clone https://github.com/YOUR_USERNAME/BolBachan.git
cd BolBachan
pip install -r requirements.txt
pip install pytest

# Verify everything works
pytest tests/ -v
python main.py examples/hello_world.bb
```

---

## Project Structure

```
src/bolbachan/
├── lexer.py         ← Add new tokens here
├── parser.py        ← Add grammar rules here
├── interpreter.py   ← Add evaluation logic here
└── errors.py        ← Add new error types here
```

---

## Making a Change

1. Fork the repo and create a branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Add or update tests in `tests/`
4. Run `pytest tests/ -v` — all tests must pass
5. Run your change against the examples: `python main.py examples/fizzbuzz.bb`
6. Open a pull request with a clear description

---

## Adding a Language Feature

Adding a new feature requires changes in three places:

### 1. Lexer (`src/bolbachan/lexer.py`)

Add the new token to the `tokens` list and define its pattern:

```python
# In the tokens list:
tokens = [..., 'MOD', ...]

# Pattern:
t_MOD_OP = r'%'   # or add to reserved dict for keyword tokens
```

### 2. Parser (`src/bolbachan/parser.py`)

Add a grammar rule:

```python
def p_expression_modulo(p):
    """expression : expression MOD expression"""
    p[0] = ('binary_op', 'mod', p[1], p[3])
```

Update the `precedence` tuple if the new operator has a specific precedence.

### 3. Interpreter (`src/bolbachan/interpreter.py`)

Handle the new AST node in `eval()` or in a helper:

```python
if op == 'mod':
    return left % right
```

### 4. Document it

- Add the new keyword/operator to `docs/grammar.md` and `docs/language-reference.md`
- Add it to the keyword table in `README.md`
- Add an example to `examples/`

---

## Writing Tests

Tests live in `tests/test_interpreter.py` and `tests/test_lexer.py`.

**Interpreter test example:**
```python
def test_modulo():
    assert get("rakho r = 10 mod 3;", "r") == 1
```

**Lexer test example:**
```python
def test_mod_token():
    assert tokenize("mod")[0] == ("MOD", "mod")
```

**Integration test (via capsys):**
```python
def test_fizzbuzz_output(capsys):
    run_file("examples/fizzbuzz.bb")
    out = capsys.readouterr().out
    assert "FizzBuzz" in out
```

---

## Code Style

- Python: follow PEP 8. Use 4-space indentation.
- BolBachan keywords: camelCase for multi-word (`badaHai`, `chhotaHai`)
- Grammar rules: one rule per function (`p_expression_logical`, `p_statement_while`)
- Error messages: should be helpful and specific — not just "error"
- Comments: use `//` in `.bb` files, `#` in Python files

---

## Submitting a Pull Request

- Keep PRs focused — one feature or fix per PR
- Include tests for any new behavior
- Update documentation for any user-visible changes
- Write a clear PR description explaining what and why

---

## Language Design Philosophy

When proposing new features, keep these principles in mind:

1. **Hinglish first** — prefer Hindi/Hinglish keywords over English ones
2. **Clarity over cleverness** — BolBachan should be readable by beginners
3. **Minimal syntax** — avoid adding operators that can be expressed with existing ones
4. **Pedagogical value** — since this is a teaching language, features should illustrate programming paradigms clearly
5. **Consistency** — new syntax should feel like it belongs with existing syntax

---

Questions? Open an issue or discussion. Dhanyavaad! 🙏
