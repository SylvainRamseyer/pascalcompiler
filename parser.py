import ply.yacc as yacc

from lex import tokens

# operations = {
#     '+': lambda x, y: x+y,
#     '-': lambda x, y: x-y,
#     '*': lambda x, y: x*y,
#     '/': lambda x, y: x/y,
# )


def p_expression(p):
    """ expression : expression_int
        | expression_real """
    p[0] = p[1]


def p_expression_int(p):
    """ expression_int : INTEGER
        | INTEGER ';' expression """
    p[0] = p[1]


def p_expression_real(p):
    """ expression_real : REAL
        | REAL ';' expression """
    p[0] = p[1]


def p_error(p):
    print("Syntax error in line %d" % p.lineno)
    parser.errok()

# precedence = (
#     ('left', 'ADD_OP'),
#     ('left', 'MUL_OP'),
#     ('right', 'UMINUS'),
# )


parser = yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys
    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog, debug=1)
    print(result)
