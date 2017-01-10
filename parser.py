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
    p[0] = AST.FileNode(P[1])


# PROGRAM declaration : PROGRAM program_name;
def p_program(p):
    """ program : PROGRAM IDENTIFIER  ';' block '.' """
    p[0] = AST.ProgramNode(p[3],p[1])

# BLOCK :
def p_block(p):
    """ block : VAR declaration_part statement_part """
    p[0] = p[1]

def p_declaration_part

def p_var_declaration(p):
    """ statement : IDENTIFIER ':' type """
    variables[p[2]] = ""
    p[0] = p[1]


def p_type(p):
    """ type : INTEGER
        | REAL """
    p[0] = p[1]


# EXPRESSION : arithmetic operators
def p_statement_int_op(p):
    """ statement : INTEGER_VALUE ADD_OP INTEGER_VALUE
        | INTEGER_VALUE MUL_OP INTEGER_VALUE """
    p[0] = operations[p[2]](int(p[1]), int(p[3]))
    print("P 0 : ", p[0])
    print("P 1 : ", p[1])
    print("P 2 : ", p[2])
    print("P 3 : ", p[3])


def p_statement_float_op(p):
    """ statement : REAL_VALUE ADD_OP REAL_VALUE
        | REAL_VALUE MUL_OP REAL_VALUE """
    p[0] = operations[p[2]](float(p[1]), float(p[3]))
    print("P 0 : ", p[0])
    print("P 1 : ", p[1])
    print("P 2 : ", p[2])
    print("P 3 : ", p[3])


def p_minus(p):
    """ statement : ADD_OP statement %prec UMINUS """
    p[0] = operations[p[1]](0, int(p[2]))


def p_assignation(p):
    """ statement : assignation """
    p[0] = p[1]


# ASSIGNATION : toto = expression
def p_assign(p):
    """ assignation : IDENTIFIER '=' statement """
    # (dictionary) : id(key), expression(value)
    if variables.get(p[1], None) is None:
        exit('Unknown variable "%s" at line %d.' % (p[1], p.lineno(1)))
    variables[p[1]] = p[3]
    print(p[1], "contains", p[3])
    p[0] = p[3]


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
    """ statement : INTEGER_VALUE """
    p[0] = p[1]


# STATEMENT : variable type : REAL
def p_statement_real(p):
    """ statement : REAL_VALUE """
    p[0] = p[1]


def p_statement_char(p):
    """  statement : CHAR_VALUE """
    p[0] = p[1]


def p_write(p):
    """ statement : WRITE '(' statement ')' """
    p[0] = p[2]


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
    print("Here are your variables")
    print(variables)
