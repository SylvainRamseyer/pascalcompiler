import ply.yacc as yacc

from lex import tokens


def p_file(p):
    ''' file : program '''
    p[0] = p[1]


def p_program(p):
    ''' program : PROGRAM IDENTIFIER  ';' block '.' '''
    p[0] = p[3]


def p_block(p):
    ''' block : BEGIN statement END '''
    p[0] = p[2]


def p_statement(p):
    ''' statement : statement ';' statement
        | statement ';' '''
    p[0] = p[1]


def p_statement_int(p):
    ''' statement : INTEGER '''
    p[0] = p[1]


def p_error(p):
    print("Syntax error in line %d" % p.lineno)
    parser.errok()


parser = yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys
    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog, debug=1)
    print(result)
