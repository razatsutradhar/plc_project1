import ply.lex as lex


reserved = {}

tokens = ['CHAR', 'LPAR', 'RPAR', 'UNION', 'KLEENE', 'SEMI'] + list(reserved.values())

t_LPAR = r'\('
t_RPAR = r'\)'
t_UNION = r'\+'
t_KLEENE = r'\*'
t_SEMI = r';'

t_ignore = " \r\n\t,"


def t_CHAR(t):
    r'[a-zA-Z0-9#]'
    t.value = str(t.value)
    return t


def t_error(t):
    print("error: ")
    print(t.value[0])
    raise Exception('LEX ERROR')


lexer = lex.lex()
