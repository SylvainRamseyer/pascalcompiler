import ply.yacc as yacc
import AST
from lexer import tokens

# OPERATIONS : dictionary
operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y
}


# dictionary
variables = {}


# FILE : program entry
def p_file(p):
    """ file : program """
    p[0] = p[1]


# PROGRAM declaration : PROGRAM program_name;
def p_program(p):
    """ program : PROGRAM IDENTIFIER  ';' block '.' """
    p[0] = p[3]


# BLOCK :
def p_block(p):
    """ block : statement_part """
    p[0] = p[1]


# EXPRESSION : arithmetic operators
def p_expression_op(p):
    """ expression : statement ADD_OP statement
        | statement MUL_OP statement """
    p[0] = operations[p[2]](p[1], p[3])


def p_minus(p):
    """ statement : ADD_OP statement %prec UMINUS """
    p[0] = operations[p[1]](0, p[2])


# ASSIGNATION : toto = expression
def p_assign(p):
    """ assignation : IDENTIFIER '=' statement """
    # (dictionary) : id(key), expression(value)
    variables[p[1]] = p[3]
    p[0] = p[3]

# VARIABLE declaration : VAR variable : variable_type;
# def p_variable_declaration(p):
#     """ variable_declaration : IDENTIFIER ':' BOOLEAN ';' """
#     # TODO
#     raise NotImplementedError
#
#
# # VARIABLE declaration : nested OR no vars
# def p_variable_declaration_part(p):
#     """ variable_declaration_part : VAR variable_declaration_list ';'
#         | """
#     if p[0]:
#         p[0] = p[2]
#
#
# # VARIABLE declaration list : nested variables
# def p_variable_declaration_list(p):
#     """ variable_declaration_list : variable_declaration_list ';' variable_declaration
#         | variable_declaration """
#     p[0] = p[1]
#     # TODO
#     # raise NotImplementedError


# STATEMENT : block
def p_statement_part(p):
    """ statement_part : BEGIN statement END """
    p[0] = p[2]


# STATEMENT : nested statement
def p_statement(p):
    """ statement : statement ';' statement
        | statement ';' """
    p[0] = p[1]


# STATEMENT : variable type : INT
def p_statement_int(p):
    """ statement : INTEGER """
    p[0] = p[1]


# STATEMENT : variable type : REAL
def p_statement_real(p):
    """ statement : REAL """
    p[0] = p[1]


# ERROR check
def p_error(p):
    print("Syntax error in line %d" % p.lineno)
    parser.errok()


# LEXEMES : priority rules
precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS'),
)

parser = yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys
    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog, debug=1)
    print(result)
