"""
BolBachan Lexer
===============
Tokenizes BolBachan source code using PLY (Python Lex-Yacc).

Keyword mapping (Hinglish → English concept):
  rakho       → assign/let
  bolBhai     → print
  agar        → if
  toh         → then
  nahiToh     → else
  jabTak      → while
  baarBaar    → for
  jodo        → + (add)
  ghatao      → - (subtract)
  guna        → * (multiply)
  bhaag       → / (integer divide)
  badaHai     → > (greater than)
  chhotaHai   → < (less than)
  barabarHai  → == (equal)
  wapis       → return
  function    → function definition
  sahi        → true
  galat       → false
"""

import ply.lex as lex

# ---------------------------------------------------------------------------
# Reserved keywords  (BolBachan keywords only — no English identifiers here)
# ---------------------------------------------------------------------------
reserved = {
    "rakho":       "ASSIGN",
    "bolBhai":     "PRINT",
    "agar":        "AGAR",
    "toh":         "TOH",
    "nahiToh":     "NAHITOH",
    "jabTak":      "JABTAK",
    "baarBaar":    "BAARBAAR",
    "int":         "TYPE",
    "bool":        "TYPE",
    "string":      "TYPE",
    "float":       "TYPE",
    "true":        "BOOL",
    "false":       "BOOL",
    "sahi":        "BOOL",      # Hindi alias for true
    "galat":       "BOOL",      # Hindi alias for false
    "badaHai":     "GT",
    "chhotaHai":   "LT",
    "barabarHai":  "EQ",
    "naBrabar":    "NEQ",       # not-equal operator
    "jodo":        "PLUS",
    "ghatao":      "MINUS",
    "guna":        "TIMES",
    "bhaag":       "DIVIDE",
    "function":    "FUNCTION",
    "wapis":       "RETURN",
}

# ---------------------------------------------------------------------------
# Token list  (reserved keyword tokens are added automatically below)
# ---------------------------------------------------------------------------
_reserved_tokens = list(set(reserved.values()))

tokens = _reserved_tokens + [
    "ID",
    "NUMBER",
    "FLOAT_NUM",
    "STRING",
    # Arithmetic symbols
    "INCR",
    "DECR",
    # Assignment / misc
    "ASSIGN_OP",
    "QMARK",
    "COLON",
    # Grouping
    "LPAREN",
    "RPAREN",
    "LBRACE",
    "RBRACE",
    # Punctuation
    "SEMI",
    "COMMA",
    # Logical
    "AND",
    "OR",
    "NOT",
]

# ---------------------------------------------------------------------------
# Simple symbol rules  (order matters: longer patterns must come first)
# ---------------------------------------------------------------------------
t_INCR     = r"\+\+"
t_DECR     = r"--"
t_AND      = r"&"
t_OR       = r"\|"
t_NOT      = r"!"
t_ASSIGN_OP = r"="
t_QMARK    = r"\?"
t_COLON    = r":"
t_LPAREN   = r"\("
t_RPAREN   = r"\)"
t_LBRACE   = r"\{"
t_RBRACE   = r"\}"
t_SEMI     = r";"
t_COMMA    = r","

# ---------------------------------------------------------------------------
# Complex token rules
# ---------------------------------------------------------------------------

def t_COMMENT(t):
    r"//[^\n]*"
    # Discard line comments — do not return the token
    pass


def t_FLOAT_NUM(t):
    r"\d+\.\d+"
    t.value = float(t.value)
    return t


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]   # strip surrounding quotes
    return t


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    # Map to a keyword token type if it is a reserved word
    t.type = reserved.get(t.value, "ID")
    return t


# ---------------------------------------------------------------------------
# Whitespace and newlines
# ---------------------------------------------------------------------------
t_ignore = " \t\r"


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# ---------------------------------------------------------------------------
# Error handler
# ---------------------------------------------------------------------------
def t_error(t):
    from .errors import LexError
    raise LexError(
        f"Unrecognized character '{t.value[0]}'",
        line=t.lexer.lineno,
    )


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------
def make_lexer(debug=False):
    """Return a fresh PLY lexer instance."""
    return lex.lex(debug=debug, errorlog=lex.NullLogger() if not debug else None)
