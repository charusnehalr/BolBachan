"""
BolBachan Parser
================
Builds an Abstract Syntax Tree (AST) from a token stream using PLY yacc.

AST node format (all nodes are tuples):
  ('program',       [stmt, ...])
  ('declare',       type_str, var_name)
  ('assign',        var_name, expr_node)
  ('print',         expr_node)
  ('if_else',       cond, then_block, else_block)
  ('if',            cond, then_block)
  ('while',         cond, body)
  ('for',           init, cond, post, body)
  ('function_def',  name, [param, ...], body)
  ('function_call', name, [arg, ...])
  ('return',        expr_node)
  ('binary_op',     op_keyword, left, right)
  ('relational_op', op_keyword, left, right)
  ('logical_op',    op_symbol, left, right)
  ('unary_op',      op_symbol, var_name)
  ('ternary',       cond, true_expr, false_expr)
  ('number',        int_value)
  ('float',         float_value)
  ('string',        str_value)
  ('bool',          bool_value)
  ('var',           name)
"""

import os
import ply.yacc as yacc

# PLY requires `tokens` to be importable from the grammar module's namespace
from .lexer import tokens  # noqa: F401

# ---------------------------------------------------------------------------
# Operator precedence  (lowest → highest, left-assoc unless noted)
# ---------------------------------------------------------------------------
precedence = (
    ("right", "QMARK", "COLON"),     # ternary  a ? b : c
    ("left",  "OR"),                  # |
    ("left",  "AND"),                 # &
    ("right", "NOT"),                 # !  (unary, right-assoc)
    ("nonassoc", "EQ", "NEQ"),        # barabarHai, naBrabar
    ("nonassoc", "GT", "LT"),         # badaHai, chhotaHai
    ("left",  "PLUS", "MINUS"),       # jodo, ghatao
    ("left",  "TIMES", "DIVIDE"),     # guna, bhaag
)

# ---------------------------------------------------------------------------
# Grammar rules
# ---------------------------------------------------------------------------

def p_program(p):
    """program : statement_list"""
    stmts = p[1]
    # Hoist function definitions before other statements
    # so functions can be defined anywhere in a file and still be callable
    func_defs = [s for s in stmts if isinstance(s, tuple) and s[0] == "function_def"]
    others    = [s for s in stmts if not (isinstance(s, tuple) and s[0] == "function_def")]
    p[0] = ("program", func_defs + others)


def p_statement_list_multi(p):
    """statement_list : statement_list statement"""
    p[0] = p[1] + [p[2]] if p[2] is not None else p[1]


def p_statement_list_single(p):
    """statement_list : statement"""
    p[0] = [p[1]] if p[1] is not None else []


def p_statement_list_empty(p):
    """statement_list : empty"""
    p[0] = []


# --- Declarations & Assignments ---

def p_statement_declaration(p):
    """statement : TYPE ID SEMI"""
    p[0] = ("declare", p[1], p[2])


def p_statement_assignment(p):
    """statement : ASSIGN ID ASSIGN_OP expression SEMI"""
    p[0] = ("assign", p[2], p[4])


def p_assignment_no_semi(p):
    """assignment : ID ASSIGN_OP expression"""
    p[0] = ("assign", p[1], p[3])


# --- Output ---

def p_statement_print(p):
    """statement : PRINT LPAREN expression RPAREN SEMI"""
    p[0] = ("print", p[3])


# --- Control Flow ---

def p_statement_if_else(p):
    """statement : AGAR LPAREN expression RPAREN TOH LBRACE statement_list RBRACE NAHITOH LBRACE statement_list RBRACE"""
    p[0] = ("if_else", p[3], p[7], p[11])


def p_statement_if(p):
    """statement : AGAR LPAREN expression RPAREN TOH LBRACE statement_list RBRACE"""
    p[0] = ("if", p[3], p[7])


def p_statement_while(p):
    """statement : JABTAK LPAREN expression RPAREN LBRACE statement_list RBRACE"""
    p[0] = ("while", p[3], p[6])


def p_statement_for(p):
    """statement : BAARBAAR LPAREN statement expression SEMI assignment RPAREN LBRACE statement_list RBRACE"""
    p[0] = ("for", p[3], p[4], p[6], p[9])


# --- Functions ---

def p_statement_function_def(p):
    """statement : FUNCTION ID LPAREN parameter_list RPAREN LBRACE statement_list RBRACE"""
    p[0] = ("function_def", p[2], p[4], p[7])


def p_parameter_list_multi(p):
    """parameter_list : parameter_list COMMA ID"""
    p[0] = p[1] + [p[3]]


def p_parameter_list_single(p):
    """parameter_list : ID"""
    p[0] = [p[1]]


def p_parameter_list_empty(p):
    """parameter_list : empty"""
    p[0] = []


def p_statement_return(p):
    """statement : RETURN expression SEMI"""
    p[0] = ("return", p[2])


# --- Expressions ---

def p_expression_ternary(p):
    """expression : expression QMARK expression COLON expression"""
    p[0] = ("ternary", p[1], p[3], p[5])


def p_expression_logical(p):
    """expression : expression AND expression
                  | expression OR  expression"""
    p[0] = ("logical_op", p[2], p[1], p[3])


def p_expression_not(p):
    """expression : NOT expression"""
    p[0] = ("not_op", p[2])


def p_expression_relational(p):
    """expression : expression GT  expression
                  | expression LT  expression
                  | expression EQ  expression
                  | expression NEQ expression"""
    p[0] = ("relational_op", p[2], p[1], p[3])


def p_expression_arithmetic(p):
    """expression : expression PLUS   expression
                  | expression MINUS  expression
                  | expression TIMES  expression
                  | expression DIVIDE expression"""
    p[0] = ("binary_op", p[2], p[1], p[3])


def p_expression_increment(p):
    """expression : ID INCR
                  | ID DECR"""
    p[0] = ("unary_op", p[2], p[1])


def p_expression_group(p):
    """expression : LPAREN expression RPAREN"""
    p[0] = p[2]


def p_expression_function_call(p):
    """expression : ID LPAREN argument_list RPAREN"""
    p[0] = ("function_call", p[1], p[3])


def p_argument_list_multi(p):
    """argument_list : argument_list COMMA expression"""
    p[0] = p[1] + [p[3]]


def p_argument_list_single(p):
    """argument_list : expression"""
    p[0] = [p[1]]


def p_argument_list_empty(p):
    """argument_list : empty"""
    p[0] = []


def p_expression_number(p):
    """expression : NUMBER"""
    p[0] = ("number", p[1])


def p_expression_float(p):
    """expression : FLOAT_NUM"""
    p[0] = ("float", p[1])


def p_expression_string(p):
    """expression : STRING"""
    p[0] = ("string", p[1])


def p_expression_bool(p):
    """expression : BOOL"""
    p[0] = ("bool", p[1] in ("true", "sahi"))


def p_expression_variable(p):
    """expression : ID"""
    p[0] = ("var", p[1])


def p_empty(p):
    """empty :"""
    p[0] = None


# ---------------------------------------------------------------------------
# Error rule
# ---------------------------------------------------------------------------

def p_error(p):
    from .errors import ParseError
    if p:
        raise ParseError(
            f"Unexpected token '{p.value}' ({p.type})",
            line=p.lineno,
        )
    else:
        raise ParseError("Unexpected end of file — did you forget a ';' or '}'?")


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def make_parser(debug=False):
    """Return a fresh PLY parser instance."""
    _dir = os.path.dirname(os.path.abspath(__file__))
    return yacc.yacc(
        debug=debug,
        outputdir=_dir,
        errorlog=yacc.NullLogger() if not debug else None,
    )
