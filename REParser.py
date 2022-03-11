import ply.yacc as yacc
from RELexer import tokens


def p_start_1(p):
    'starter : exprUN SEMI'
    p[0] = p[1]


def p_exprCAT_1(p):
    'exprCAT : exprCAT exprCAT'
    p[0] = ['cat', p[1], p[2]]


def p_exprCAT_2(p):
    'exprCAT : LPAR exprCAT RPAR'
    p[0] = p[2]


def p_exprCAT_3(p):
    'exprCAT : exprKLE'
    p[0] = p[1]


def p_exprUN_1(p):
    'exprUN : exprUN UNION exprCAT'
    p[0] = ['union', p[1], p[3]]


def p_exprUN_2(p):
    'exprUN : exprCAT'
    p[0] = p[1]


def p_exprUN_3(p):
    'exprUN : LPAR exprUN RPAR'
    p[0] = p[2]



def p_exprKLE_1(p):
    'exprKLE : exprKLE KLEENE'
    p[0] = ['kleene', p[1]]


def p_exprKLE_2(p):
    'exprKLE : exprUN KLEENE'
    p[0] = ['kleene', p[1]]


def p_exprKLE_3(p):
    'exprKLE : exprCAT KLEENE'
    p[0] = ['kleene', p[1]]


def p_exprKLE_4(p):
    'exprKLE : LPAR exprKLE RPAR'
    p[0] = p[2]


def p_exprKLE_5(p):
    'exprKLE : expr'
    p[0] = p[1]


def p_expr_1(p):
    'expr : LPAR expr RPAR'
    p[0] = p[2]



def p_expr_2(p):
    'expr : CHAR'
    p[0] = ['char', p[1]]


def p_error(p):
    print("Syntax error in input!")


parser = yacc.yacc()