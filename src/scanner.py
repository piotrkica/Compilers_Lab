import ply.lex as lex

literals = ['+', '-', '*', '/', '(', ')', '[', ']', '{', '}', '=', ';', ':', ',', '\'']

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
    'print': 'PRINT',
}

tokens = [
    # MATRIX BINARY OPERATORS
    'DOTADD',
    'DOTSUB',
    'DOTMUL',
    'DOTDIV',
    # ASSIGN OPERATORS
    'PLUSASSIGN',
    'SUBASSIGN',
    'MULASSIGN',
    'DIVASSIGN',
    # RELATIONAL OPERATORS
    'LESSER_THAN',
    'GREATER_THAN',
    'LESSER_EQUAL',
    'GREATER_EQUAL',
    'NOT_EQUAL',
    'EQUAL',
    # OTHER
    'ID',
    'FLOATNUM',
    'INTNUM',
    'STRING',
] + list(reserved.values())


t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'

t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'

t_PLUSASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'\/='

t_LESSER_THAN = r'\<'
t_GREATER_THAN = r'\>'
t_LESSER_EQUAL = r'\<='
t_GREATER_EQUAL = r'\>='
t_NOT_EQUAL = r'\!='
t_EQUAL = r'\=='


def t_STRING(t):
    r"""\"""(.|\n)*?""\"|\'\'\'(.|\n)*?\'\'\'|".*?"|'.*?'"""
    if t.value[:3] == '"""' or t.value[:3] == "'''":
        t.value = t.value[3:-3]
    else:
        t.value = t.value[1:-1]
    return t


def t_ID(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t


def t_FLOATNUM(t):
    r'([0-9]*[\.][0-9]+|[0-9]+[\.][0-9]*)((E|e)(\+|-)?[0-9]+)?|([0-9]+)((E|e)(\+|-)?[0-9]+)'
    #  .0 cases       OR  0. cases     AND maybe exp notation OR int with exp notation
    t.value = float(t.value)
    return t


def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("line %d: illegal character '%s'" % (t.lineno, t.value[0]))
    t.lexer.skip(1)


lexer = lex.lex()
