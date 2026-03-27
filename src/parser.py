import ply.yacc as yacc
from lexer import tokens

parse_tree = []

def p_program(p):
    '''program : statement_list'''
    # Hoist all function_def nodes to the front at the program level as well
    stmts = p[1]
    func_defs = [s for s in stmts if isinstance(s, tuple) and s[0] == 'function_def']
    non_funcs = [s for s in stmts if not (isinstance(s, tuple) and s[0] == 'function_def')]
    p[0] = ('program', func_defs + non_funcs)
    global parse_tree
    parse_tree = p[0]

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement
                      | empty'''
    if len(p) == 3:
        if p[1] is None:
            p[0] = [p[2]]
        elif p[2] is None:
            p[0] = p[1]
        else:
            # Hoist all function_def nodes to the front, preserving order
            p0 = p[1] + [p[2]]
            func_defs = [s for s in p0 if isinstance(s, tuple) and s[0] == 'function_def']
            non_funcs = [s for s in p0 if not (isinstance(s, tuple) and s[0] == 'function_def')]
            p[0] = func_defs + non_funcs
    elif len(p) == 2:
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]
    else:
        p[0] = []

def p_statement_declaration(p):
    'statement : TYPE ID SEMI'
    p[0] = ('declare', p[1], p[2])

def p_statement_assignment(p):
    'statement : ASSIGN ID ASSIGN_OP expression SEMI'
    p[0] = ('assign', p[2], p[4])

def p_assignment(p):
    'assignment : ID ASSIGN_OP expression'
    p[0] = ('assign', p[1], p[3])

def p_statement_print(p):
    'statement : PRINT LPAREN expression RPAREN SEMI'
    p[0] = ('print', p[3])

def p_expression_ternary(p):
    'expression : expression QMARK expression COLON expression'
    p[0] = ('ternary', p[1], p[3], p[5])

def p_expression_logical(p):
    '''expression : expression AND expression
                  | expression OR expression'''
    p[0] = ('logical_op', p[2], p[1], p[3])

def p_expression_relational(p):
    '''expression : expression GT expression
                  | expression LT expression
                  | expression EQ expression'''
    p[0] = ('relational_op', p[2], p[1], p[3])

def p_expression_arithmetic(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = ('binary_op', p[2], p[1], p[3])

def p_expression_increment(p):
    '''expression : ID INCR
                  | ID DECR'''
    p[0] = ('unary_op', p[2], p[1])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ('number', p[1])

def p_expression_string(p):
    'expression : STRING'
    p[0] = ('string', p[1])

def p_expression_bool(p):
    'expression : BOOL'
    p[0] = ('bool', p[1])

def p_statement_if_else(p):
    '''statement : AGAR LPAREN expression RPAREN TOH LBRACE statement_list RBRACE NAHITOH LBRACE statement_list RBRACE'''
    p[0] = ('if_else', p[3], p[7], p[11])

def p_statement_while(p):
    '''statement : JABTAK LPAREN expression RPAREN LBRACE statement_list RBRACE'''
    p[0] = ('while', p[3], p[6])

def p_statement_for(p):
    '''statement : BAARBAAR LPAREN statement expression SEMI assignment RPAREN LBRACE statement_list RBRACE
                 | BAARBAAR LPAREN statement expression SEMI assignment RPAREN LBRACE empty RBRACE'''
    if len(p) == 11:
        p[0] = ('for', p[3], p[4], p[6], p[9])
    else:
        p[0] = ('for', p[3], p[4], p[6], [])

def p_for_init(p):
    '''for_init : statement
                | declaration'''
    p[0] = p[1]

def p_declaration(p):
    'declaration : ASSIGN ID ASSIGN_OP expression SEMI'
    p[0] = ('assign', p[2], p[4])

def p_expression_variable(p):
    'expression : ID'
    p[0] = ('var', p[1])

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

def p_function_definition(p):
    'statement : FUNCTION ID LPAREN parameter_list RPAREN LBRACE statement_list RBRACE'
    p[0] = ('function_def', p[2], p[4], p[7])

def p_parameter_list(p):
    '''parameter_list : parameter_list COMMA ID
                      | ID
                      | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]

def p_function_call(p):
    'expression : ID LPAREN argument_list RPAREN'
    p[0] = ('function_call', p[1], p[3])

def p_argument_list(p):
    '''argument_list : argument_list COMMA expression
                     | expression
                     | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]

def p_statement_return(p):
    'statement : RETURN expression SEMI'
    p[0] = ('return', p[2])

def p_empty(p):
    'empty :'
    p[0] = None

parser = yacc.yacc()
