import ply.lex as lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT'
}

tokens = [
    'DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV',
    'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN',
    'LE', 'GE', 'NE', 'EQ',
    'ID',
    'FLOATNUM',
    'INTNUM',
    'STRING'
] + list(reserved.values())

# Tokens

t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'

t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='

t_LE = r'<='
t_GE = r'>='
t_NE = r'!='
t_EQ = r'=='

literals = "+-*/=<>()[]{}:',;"

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

def t_FLOATNUM(t):
    r'((\.\d+)|(\d+\.\d*))([eE][+-]?\d+)?'
    return t

def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"([^"\\\n]|(\\.))*\"'
    return t

# Ignored characters
t_ignore = " \t"
t_ignore_COMMENT = r'\#.*'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Error handling rule
def t_error(t):
    print(f"{t.lexer.lineno}: Illegal character {t.value[0]!r}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
