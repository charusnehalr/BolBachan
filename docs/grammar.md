# BolBachan Formal Grammar (EBNF)

This document specifies the complete grammar of BolBachan v1.0 in Extended Backus–Naur Form (EBNF).

---

## Notation

| Symbol | Meaning |
|--------|---------|
| `::=`  | is defined as |
| `|`    | alternation (or) |
| `{ }` | zero or more repetitions |
| `[ ]` | optional (zero or one) |
| `( )` | grouping |
| `" "` | terminal string literal |

---

## Top-Level

```ebnf
program       ::= { statement } ;

statement     ::= declaration
               |  assignment_stmt
               |  print_stmt
               |  if_stmt
               |  while_stmt
               |  for_stmt
               |  function_def
               |  return_stmt
               ;
```

---

## Declarations & Assignments

```ebnf
declaration     ::= type ID ";" ;

assignment_stmt ::= "rakho" ID "=" expression ";" ;

assignment      ::= ID "=" expression ;   (* used in for-loop post step *)

type            ::= "int" | "bool" | "string" | "float" ;
```

---

## Output

```ebnf
print_stmt ::= "bolBhai" "(" expression ")" ";" ;
```

---

## Control Flow

```ebnf
if_stmt ::= "agar" "(" expression ")" "toh" "{" { statement } "}"
             [ "nahiToh" "{" { statement } "}" ] ;

while_stmt ::= "jabTak" "(" expression ")" "{" { statement } "}" ;

for_stmt ::= "baarBaar" "(" assignment_stmt expression ";" assignment ")"
              "{" { statement } "}" ;
```

---

## Functions

```ebnf
function_def ::= "function" ID "(" parameter_list ")" "{" { statement } "}" ;

parameter_list ::= ID { "," ID }
                |  (* empty *) ;

return_stmt ::= "wapis" expression ";" ;
```

---

## Expressions

Operator precedence (highest to lowest):

| Level | Operator(s) | Associativity |
|-------|-------------|---------------|
| 7 | `( expr )` — grouping | — |
| 6 | `ID++`, `ID--` — post-increment/decrement | left |
| 5 | `jodo ghatao guna bhaag` — arithmetic | left |
| 4 | `badaHai chhotaHai barabarHai naBrabar` — relational | non-assoc |
| 3 | `!` — logical NOT | right (unary) |
| 2 | `&` — logical AND | left |
| 1 | `\|` — logical OR | left |
| 0 | `? :` — ternary | right |

```ebnf
expression    ::= expression "?" expression ":" expression      (* ternary *)
               |  expression "|" expression                      (* logical or *)
               |  expression "&" expression                      (* logical and *)
               |  "!" expression                                  (* logical not *)
               |  expression relational_op expression            (* comparison *)
               |  expression arithmetic_op expression            (* arithmetic *)
               |  ID "++"                                        (* post-increment *)
               |  ID "--"                                        (* post-decrement *)
               |  "(" expression ")"                             (* grouping *)
               |  ID "(" argument_list ")"                       (* function call *)
               |  ID                                             (* variable *)
               |  NUMBER                                         (* integer literal *)
               |  FLOAT_NUM                                      (* float literal *)
               |  STRING                                         (* string literal *)
               |  boolean                                        (* boolean literal *)
               ;

arithmetic_op  ::= "jodo" | "ghatao" | "guna" | "bhaag" ;
relational_op  ::= "badaHai" | "chhotaHai" | "barabarHai" | "naBrabar" ;

argument_list  ::= expression { "," expression }
               |  (* empty *) ;

boolean        ::= "true" | "false" | "sahi" | "galat" ;
```

---

## Lexical Tokens

```ebnf
ID         ::= [a-zA-Z_] [a-zA-Z0-9_]* ;
NUMBER     ::= [0-9]+ ;
FLOAT_NUM  ::= [0-9]+ "." [0-9]+ ;
STRING     ::= '"' [^"\n]* '"' ;
COMMENT    ::= "//" [^\n]* ;      (* discarded by lexer *)
```

### Keywords (reserved — cannot be used as identifiers)

| BolBachan | English equivalent |
|-----------|--------------------|
| `rakho`      | let / assign |
| `bolBhai`    | print |
| `agar`       | if |
| `toh`        | then |
| `nahiToh`    | else |
| `jabTak`     | while |
| `baarBaar`   | for |
| `jodo`       | + (add) |
| `ghatao`     | − (subtract) |
| `guna`       | × (multiply) |
| `bhaag`      | ÷ (integer divide) |
| `badaHai`    | > (greater than) |
| `chhotaHai`  | < (less than) |
| `barabarHai` | == (equal) |
| `naBrabar`   | != (not equal) |
| `true`       | boolean true |
| `false`      | boolean false |
| `sahi`       | boolean true (Hindi) |
| `galat`      | boolean false (Hindi) |
| `function`   | function definition |
| `wapis`      | return |
| `int`        | integer type hint |
| `bool`       | boolean type hint |
| `string`     | string type hint |
| `float`      | float type hint |

---

## Example: Grammar in Action

```
// Source
function add(a, b) {
    wapis a jodo b;
}
rakho result = add(3, 4);
bolBhai(result);

// Parse tree (simplified)
(program
  (function_def "add" ["a" "b"]
    [(return (binary_op "jodo" (var "a") (var "b")))])
  (assign "result"
    (function_call "add" [(number 3) (number 4)]))
  (print (var "result")))
```
