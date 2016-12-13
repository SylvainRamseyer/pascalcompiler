import ply.yacc as yacc
import AST
from lex import tokens

# variable dictionary
vars = {}

# def p_programme_statement(p):
#     ''' programme : PROGRAM IDENTIFIER ';' block '.' '''
#     print(p)
#     #p[0] = AST.ProgramNode(p[1])
#
# def p_block(p):
#     ''' block : BEGIN statement END '''
#     p[0] = AST.ProgramNode(p[1])
#
# def p_statement(p):
#     ''' statement : assignation
#         | structure '''
#     p[0] = p[1]

# ERROR MANAGEMENT
def p_error(p):
    if p:
        print("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print("Sytax error: unexpected end of file!")


# PARSING
def parse(program):
    return yacc.parse(program)

# PRIORITY RULES
precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS'),
)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)
    if result:
        print(result)

        import os
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
        graph.write_pdf(name)
        print("wrote ast to", name)
    else:
        print("Parsing returned no result!")
