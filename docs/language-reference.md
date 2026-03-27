# BolBachan Language Reference

**Version:** 1.0
**Paradigm:** Imperative / Procedural with functional function calls
**Extension:** `.bb`

---

## Table of Contents

1. [Variables](#variables)
2. [Data Types](#data-types)
3. [Operators](#operators)
4. [Conditionals](#conditionals)
5. [Loops](#loops)
6. [Functions](#functions)
7. [Output](#output)
8. [Comments](#comments)
9. [Error Messages](#error-messages)

---

## Variables

BolBachan uses `rakho` (Hindi: "keep/place") to create and update variables. There is no separate declaration requirement — `rakho` serves both purposes.

```bolbachan
rakho name = "Arjun";
rakho age  = 25;
rakho score = 98.5;
rakho passed = true;
```

Optional type hints (not enforced at runtime, but document intent):

```bolbachan
int x;
bool flag;
string greeting;
float pi;

rakho x        = 42;
rakho flag     = true;
rakho greeting = "Namaste";
rakho pi       = 3.14;
```

### Assignment rules

- `rakho x = expr;` — creates `x` if it does not exist, or updates it if it does.
- Scope: global by default. Inside a function, variables are local.
- Variables are dynamically typed — the type is the type of the assigned value.

---

## Data Types

| Type | Example | Notes |
|------|---------|-------|
| Integer | `42`, `0`, `-7` | Whole numbers. Negative via `0 ghatao 7`. |
| Float | `3.14`, `0.5` | Decimal numbers. Division of ints gives int result. |
| String | `"Namaste"` | UTF-8, double-quoted. No escape sequences yet. |
| Boolean | `true` / `sahi`, `false` / `galat` | Both spellings are valid. Printed as `sahi`/`galat`. |
| Null | `khaali` | Printed when a variable has no value (forward declaration). |

---

## Operators

### Arithmetic

| Operator | Symbol | Example | Result |
|----------|--------|---------|--------|
| Add      | `jodo`   | `3 jodo 4` | `7` |
| Subtract | `ghatao` | `10 ghatao 3` | `7` |
| Multiply | `guna`   | `6 guna 7` | `42` |
| Int-Divide | `bhaag` | `10 bhaag 3` | `3` |

`jodo` also concatenates strings:
```bolbachan
rakho greeting = "Hello, " jodo "World!";   // "Hello, World!"
rakho info = "Score: " jodo 95;             // "Score: 95"
```

### Relational

| Operator | Meaning | Example |
|----------|---------|---------|
| `badaHai`    | greater than `>` | `x badaHai 5` |
| `chhotaHai`  | less than `<`    | `x chhotaHai 10` |
| `barabarHai` | equal `==`       | `x barabarHai 0` |
| `naBrabar`   | not equal `!=`   | `x naBrabar 0` |

### Logical

| Operator | Symbol | Meaning |
|----------|--------|---------|
| AND | `&` | Both sides must be true |
| OR  | `\|` | At least one side must be true |
| NOT | `!` | Negates a boolean |

```bolbachan
rakho a = true & false;     // false
rakho b = true | false;     // true
rakho c = !true;            // false
```

### Increment / Decrement

```bolbachan
rakho x = 5;
rakho y = x++;   // x becomes 6, y = 6
rakho z = x--;   // x becomes 5, z = 5
```

### Ternary

```bolbachan
rakho result = condition ? value_if_true : value_if_false;

rakho label = (score badaHai 50) ? "Pass" : "Fail";
```

### Operator Precedence (high → low)

```
Grouping:   ( expr )
Arithmetic: guna, bhaag  >  jodo, ghatao
Relational: badaHai, chhotaHai, barabarHai, naBrabar
Logical:    !  >  &  >  |
Ternary:    ? :
```

---

## Conditionals

### if-then-else

```bolbachan
agar (condition) toh {
    // runs if condition is true
} nahiToh {
    // runs if condition is false
}
```

### if-only (no else)

```bolbachan
agar (condition) toh {
    // runs if condition is true
}
```

### Chained if-else (nested)

```bolbachan
agar (score badaHai 90) toh {
    bolBhai("A+");
} nahiToh {
    agar (score badaHai 80) toh {
        bolBhai("A");
    } nahiToh {
        bolBhai("B or below");
    }
}
```

---

## Loops

### For loop — `baarBaar`

```bolbachan
baarBaar (rakho i = 0; i chhotaHai 10; i = i jodo 1) {
    bolBhai(i);
}
```

Structure: `baarBaar ( init; condition; post ) { body }`

- **init**: full statement with `rakho` (includes `;`)
- **condition**: expression evaluated before each iteration
- **post**: assignment without `;`

### While loop — `jabTak`

```bolbachan
rakho n = 10;
jabTak (n badaHai 0) {
    bolBhai(n);
    rakho n = n ghatao 1;
}
```

---

## Functions

### Definition

```bolbachan
function functionName(param1, param2) {
    // body
    wapis result;
}
```

- `function` declares the function.
- `wapis` (Hindi: "back/return") returns a value.
- Functions can be defined anywhere in the file — they are hoisted before execution.

### Calling

```bolbachan
rakho result = add(3, 4);
bolBhai(result);
```

### Recursion

BolBachan supports full recursion:

```bolbachan
function factorial(n) {
    agar (n chhotaHai 2) toh {
        wapis 1;
    }
    wapis n guna factorial(n ghatao 1);
}

bolBhai(factorial(10));   // 3628800
```

### Scoping Rules

- Parameters and `rakho` assignments inside a function are **local** to that call.
- Functions can read global variables but **cannot modify** them.
- Functions see the global environment at the time they are called.

---

## Output

```bolbachan
bolBhai(expression);
```

`bolBhai` (Hindi: "say, brother!") prints any value followed by a newline.

```bolbachan
bolBhai(42);                          // 42
bolBhai("Namaste");                   // Namaste
bolBhai(true);                        // sahi
bolBhai(false);                       // galat
bolBhai("Total: " jodo (a jodo b));   // Total: 15
```

---

## Comments

Single-line comments start with `//`:

```bolbachan
// This is a full-line comment
rakho x = 42;   // This is an inline comment
```

---

## Error Messages

BolBachan provides clear, helpful error messages:

| Situation | Error |
|-----------|-------|
| Unknown identifier | `UndefinedVariable: 'x' is not defined — did you forget 'rakho x = ...'?` |
| Unknown function | `UndefinedFunction: Function 'foo' is not defined` |
| Wrong argument count | `ArityError: 'add' expects 2 argument(s), got 1` |
| Division by zero | `DivisionByZero: Cannot divide by zero (bhaag se shoonya nahi ho sakta!)` |
| Syntax error | `ParseError: Unexpected token '=' at line 5` |
| Unknown character | `LexError: Unrecognized character '@' at line 2` |

---

## Complete Example

```bolbachan
// BolBachan — Fibonacci sequence demo

function fib(n) {
    agar (n chhotaHai 2) toh {
        wapis n;
    }
    wapis fib(n ghatao 1) jodo fib(n ghatao 2);
}

bolBhai("Fibonacci sequence:");
baarBaar (rakho i = 0; i chhotaHai 10; i = i jodo 1) {
    bolBhai("fib(" jodo i jodo ") = " jodo fib(i));
}
```

Output:
```
Fibonacci sequence:
fib(0) = 0
fib(1) = 1
fib(2) = 1
fib(3) = 2
fib(4) = 3
fib(5) = 5
fib(6) = 8
fib(7) = 13
fib(8) = 21
fib(9) = 34
```
