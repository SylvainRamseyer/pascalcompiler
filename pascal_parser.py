import ply.yacc as yacc
import AST
from lexer import tokens
from terminal_format import bcolors, print_error_message

parsing_errored = False
parsing_errors = []

# OPERATIONS : dictionary
operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    'and': lambda x, y: x and y,
    'or': lambda x, y: x or y,
}


# FILE : program entry
def p_file(p):
    """ file : program """
    p[0] = AST.FileNode(p[1])


# PROGRAM declaration : PROGRAM program_name;
def p_program(p):
    """ program : PROGRAM IDENTIFIER  ';' var_declaration_block block '.'
    | PROGRAM IDENTIFIER  ';' block '.' """
    if len(p) > 4:
        p[0] = AST.ProgramNode(p[2], [p[4], p[5]])
    else:
        p[0] = AST.ProgramNode(p[2], p[4])


# BLOCK :
def p_block(p):
    """ block : statement_part """
    p[0] = p[1]


def p_var_decl_block(p):
    """ var_declaration_block : VAR var_decl_list
    | """
    p[0] = AST.VarDeclBlockNode(p[2])


def p_var_decl_list(p):
    """ var_decl_list : var_declaration ';' var_decl_list
    | var_declaration ';' """
    if len(p) > 3:
        p[0] = AST.VarDeclListNode([p[1]]+p[3].children)
    else:
        p[0] = AST.VarDeclarationNode(p[1])


def p_var_declaration(p):
    """ var_declaration : IDENTIFIER ':' type """
    p[0] = AST.VarDeclarationNode([AST.TokenNode(p[1]), p[3]])


def p_type(p):
    """ type : INTEGER
        | BOOLEAN
        | REAL
        | CHAR """
    p[0] = AST.TypeNode(AST.TokenNode(p[1]))


# EXPRESSION : arithmetic operators
def p_statement_int_op(p):
    """ expression : expression ADD_OP expression
        | expression MUL_OP expression
        | expression AND expression
        | expression OR expression """
    p[0] = AST.OpNode(p[2], [p[1], p[3]])


def p_minus(p):
    """ expression : ADD_OP expression %prec UMINUS """
    p[0] = AST.OpNode(p[1], [p[2]])


def p_expression(p):
    """ statement : expression """
    p[0] = p[1]


def p_expression_paren(p):
    """ expression : '(' expression ')' """
    p[0] = p[2]


def p_assignation(p):
    """ statement : assignation """
    p[0] = p[1]


# ASSIGNATION : toto = expression
def p_assign(p):
    """ assignation : IDENTIFIER ':' '=' statement """
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[4]])


# STATEMENT : block
def p_statement_part(p):
    """ statement_part : BEGIN statement_list END """
    p[0] = AST.BlockNode(p[2])


# STATEMENT_LIST
def p_statement_list(p):
    """ statement_list : statement ';' statement_list
        | statement ';' """
    if len(p) > 3:
        p[0] = AST.StatementListNode([p[1]]+p[3].children)
    else:
        p[0] = AST.StatementListNode(p[1])


# STATEMENT : variable type : INT
def p_statement_int(p):
    """ expression : INTEGER_VALUE
        | REAL_VALUE
        | CHAR_VALUE
        | IDENTIFIER """
    p[0] = AST.TokenNode(p[1])


def p_write(p):
    """ statement : WRITE '(' expression ')' """
    p[0] = AST.PrintNode(p[3])


def p_while(p):
    """ statement : WHILE boolean_expression DO statement_part """
    p[0] = AST.WhileNode([p[2], p[4]])


def p_boolean_expression(p):
    """ boolean_expression : statement '<' '>' statement """
    p[0] = AST.BoolExpressionNode(p[2] + p[3], [p[1], p[4]])


# ERROR check
def p_error(p):
    global parsing_errored, parsing_errors
    parsing_errored = True
    parsing_errors.append("Syntax error in line %d" % p.lineno)
    print_error_message("Syntax error in line %d" % p.lineno)
    parser.errok()
    # raise Exception("Error while parsing"


# LEXEMES : priority rules
precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS'),
    ('left', 'AND_OP'),
    ('left', 'OR_OP')
)

parser = yacc.yacc(outputdir='generated')


def print_banner():
    print("""\

 /$$$$$$$
| $$__  $$
| $$  \ $$ /$$$$$$   /$$$$$$   /$$$$$$$  /$$$$$$   /$$$$$$
| $$$$$$$/|____  $$ /$$__  $$ /$$_____/ /$$__  $$ /$$__  $$
| $$____/  /$$$$$$$| $$  \__/|  $$$$$$ | $$$$$$$$| $$  \__/
| $$      /$$__  $$| $$       \____  $$| $$_____/| $$
| $$     |  $$$$$$$| $$       /$$$$$$$/|  $$$$$$$| $$
|__/      \_______/|__/      |_______/  \_______/|__/


                                                           """)


def parse(program):
    return yacc.parse(program)

if __name__ == "__main__":
    print_banner()
    import sys
    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog, debug=1)
    if parsing_errored:
        [print_error_message(e) for e in parsing_errors]
        exit()
    if result:
        print(result)

        import os
        graph = result.make_graphical_tree()
        name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
        graph.write_pdf(name)
        print("wrote ast to", name)
    else:
        print_error_message("Parsing returned no result!")
