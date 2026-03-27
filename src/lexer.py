import ply.lex as lex

tokens = [
    'ID', 'NUMBER', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'GT', 'LT', 'EQ',
    'AND', 'OR',
    'INCR', 'DECR',
    'ASSIGN_OP', 'QMARK', 'COLON',
    'LPAREN', 'RPAREN', 'SEMI',
    'LBRACE', 'RBRACE',
    'PRINT', 'ASSIGN', 'TYPE', 'BOOL',
    'AGAR', 'TOH', 'NAHITOH', 'JABTAK', 'BAARBAAR',
    'FUNCTION', 'RETURN', 'COMMA'
]

reserved = {
    'rakho': 'ASSIGN',
    'bolBhai': 'PRINT',
    'agar': 'AGAR',
    'toh': 'TOH',
    'nahiToh': 'NAHITOH',
    'jabTak': 'JABTAK',
    'baarBaar': 'BAARBAAR',
    'int': 'TYPE',
    'bool': 'TYPE',
    'string': 'TYPE',
    'true': 'BOOL',
    'false': 'BOOL',
    'badaHai': 'GT',
    'chhotaHai': 'LT',
    'barabarHai': 'EQ',
    'jodo': 'PLUS',
    'ghatao': 'MINUS',
    'guna': 'TIMES',
    'bhaag': 'DIVIDE',
    'function': 'FUNCTION',
    'wapis': 'RETURN'
}

t_QMARK   = r'\?'
t_COLON   = r':'
t_AND     = r'&'
t_OR      = r'\|'
t_INCR    = r'\+\+'
t_DECR    = r'\-\-'
t_ASSIGN_OP = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_SEMI    = r';'
t_LBRACE  = r'\{' 
t_RBRACE  = r'\}'
t_COMMA   = r','

def t_STRING(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]  
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

reserved_keywords = set([
    'rakho', 'bolBhai', 'agar', 'toh', 'nahiToh', 'jabTak', 'baarBaar',
    'int', 'bool', 'string', 'true', 'false', 'badaHai', 'chhotaHai', 'barabarHai',
    'jodo', 'ghatao', 'guna', 'bhaag', 'and', 'or',
    'function', 'wapis', 'print', 'assign', 'type', 'bool', 'return', 'if', 'else', 'while', 'for'
])

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    elif t.value in reserved_keywords:
        print(f"Error: '{t.value}' is a reserved keyword and cannot be used as a variable or function name.")
        t.type = 'INVALID_ID'
    return t

t_ignore = ' \t\r'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Illegal character: '{t.value[0]}'")
    t.lexer.skip(1)


lexer = lex.lex()
