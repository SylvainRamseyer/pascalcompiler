import ply.yacc as yacc
import AST

from lexer import tokens


# TODO : modification
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVISION'),
    ('left', 'OR', 'AND'),
)


"""
    PROGRAM
"""


# PROGRAM START : program entry -> recursive
def p_program_start(p):
    """ program : header ';' block '.'"""
    try:
        p[0] = AST.ProgramNode([p[1]] + p[3].children)
    except:
        p[0] = AST.ProgramNode(p[1])


# PROGRAM HEADER :
def p_header(p):
    """ header : PROGRAM identifier """
    p[0] = p[2]


"""
    BLOCK
"""


# BLOCK :
def p_block(p):
    """ block : variable_declaration_part procedure_or_function statement_part """
    p[0] = AST.BlockNode(p[1], p[2], p[3])


"""
    VARIABLES
"""


# VARIABLE declaration part
def p_variable_declaration_part(p):
    """variable_declaration_part : VAR variable_declaration_list
        | """
    if len(p) > 1:
        p[0] = p[2]


# VARIABLE declaration list
def p_variable_declaration_list(p):
    """variable_declaration_list : variable_declaration variable_declaration_list
     | variable_declaration
    """
    # function and procedure missing here
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = AST.VarListNode(p[1], p[2])


# VARIABLE declaration
def p_variable_declaration(p):
    """variable_declaration : identifier ':' type ';'"""
    p[0] = AST.VarNode(p[1], p[3])


"""
    PROCEDURE & FUNCTION
"""


# PROCEDURE OR FUNCTION
def p_procedure_or_function(p):
    """procedure_or_function : proc_or_func_declaration ';' procedure_or_function
        | """
    if len(p) == 4:
        p[0] = AST.FunctionListNode(p[1], p[3])


# PROCEDURE OR FUNCTION declaration
def p_proc_or_func_declaration(p):
    """ proc_or_func_declaration : procedure_declaration
               | function_declaration """
    p[0] = p[1]


# PROCEDURE declaration
def p_procedure_declaration(p):
    """procedure_declaration : procedure_heading ';' block"""
    p[0] = AST.ProcedureNode(p[1], p[3])


# PROCEDURE heading
def p_procedure_heading(p):
    """ procedure_heading : PROCEDURE identifier
    | PROCEDURE identifier '(' parameter_list ')'"""

    if len(p) == 3:
        p[0] = AST.ProcedureHeadNode(p[2])
    else:
        p[0] = AST.ProcedureHeadNode(p[2], p[4])


# FUNCTION declaration
def p_function_declaration(t):
    """ function_declaration : function_heading ';' block"""
    t[0] = AST.FunctionNode(t[1], t[3])


# FUNCTION heading
def p_function_heading(p):
    """ function_heading : FUNCTION type
        | FUNCTION identifier ':' type
        | FUNCTION identifier '(' parameter_list ')' : type"""
    if len(p) == 3:
        p[0] = AST.FunctionHeadNode(p[2])
    elif len(p) == 5:
        p[0] = AST.FunctionHeadNode(p[2], p[3])
    else:
        p[0] = AST.FunctionHeadNode(p[2], p[4], p[7])


"""
    PARAMETERS
"""


# PARAMETER list
def p_parameter_list(p):
    """ parameter_list : parameter ',' parameter_list
        | parameter """
    if len(p) == 4:
        p[0] = AST.ParameterListNode(p[1], p[3])
    else:
        p[0] = p[1]


# PARAMETER
def p_parameter(p):
    """ parameter : identifier ':' type"""
    p[0] = AST.ParameterNode(p[1], p[3])


# TYPE
def p_type(p):
    """ type : REAL
        | INTEGER
        | CHAR """
    p[0] = AST.TypeNode(p[1].lower())


"""
    STATEMENT
"""


# STATEMENT : block
def p_statement_part(p):
    """ statement_part : BEGIN statement_sequence END """
    p[0] = p[2]


# STATEMENT : nested statement
def p_statement_sequence(p):
    """ statement_sequence : statement ';' statement_sequence
        | statement """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = AST.StatementListNode(p[1], p[3])


# STATEMENT :
def p_statement(p):
    """statement : assignment_statement
        | statement_part
        | if_statement
        | while_statement
        | repeat_statement
        | for_statement
        | procedure_or_function_call
        |
        """
    if len(p) > 1:
        p[0] = p[1]


"""
    PROCEDURE & FUNCTION CALL
"""


# PROCEDURE OR FUNCTION call
def p_procedure_or_function_call(p):
    """ procedure_or_function_call : identifier '(' param_list ')'
        | identifier """
    if len(p) == 2:
        p[0] = AST.FunctionCallNode(p[1])
    else:
        p[0] = AST.FunctionCallNode(p[1], p[3])


# PARAMETERS list
def p_param_list(p):
    """ param_list : param_list ':' param
        | param """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = AST.ParamListNode(p[1], p[3])


# PARAMETERS
def p_param(p):
    """ param : expression """
    p[0] = AST.ParamNode(p[1])


"""
    FLOW CONTROL : STATEMENT
"""


# IF statement
def p_if_statement(p):
    """if_statement : IF expression THEN statement ELSE statement
        | IF expression THEN statement
    """
    if len(p) == 5:
        p[0] = AST.IfNode(p[2], p[4])
    else:
        p[0] = AST.IfNode(p[2], p[4], p[6])


# WHILE statement
def p_while_statement(p):
    """while_statement : WHILE expression DO statement"""
    p[0] = AST.WhileNode(p[2], p[4])


# ASSIGNMENT statement
def p_assignment_statement(p):
    """assignment_statement : identifier ASSIGNMENT expression"""
    p[0] = AST.AssignNode(p[1], p[3])


"""
    EXPRESSIONS
"""


# EXPRESSION
def p_expression(p):
    """expression : expression and_or expression_m
        | expression_m
        """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = AST.OpNode(p[2], p[1], p[3])


# TODO : modification
# EXPRESSION M : +-...
def p_expression_m(p):
    """ expression_m : expression_s
        | expression_m sign expression_s
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = AST.OpNode(p[2], p[1], p[3])


# TODO : modification
# EXPRESSION S : */
def p_expression_s(p):
    """ expression_s : element
    | expression_s psign element
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = AST.OpNode(p[2], p[1], p[3])


"""
    OPERATORS
"""


# TODO : modification
# AND / OR
def p_and_or(p):
    """ and_or : AND
        | OR """
    p[0] = AST.AndOrNode(p[1])


# TODO : modification
# SIGNS : * /
def p_psign(p):
    """psign : TIMES
        | DIVISION"""
    p[0] = AST.SignNode(p[1])


# TODO : modification
# SIGNS : + -
def p_sign(p):
    """sign : PLUS
        | MINUS
        | DIV
        """
    p[0] = AST.SignNode(p[1])


# TODO : modification
# ELEMENTS
def p_element(p):
    """element : identifier
        | real
        | integer
        | char
        | '(' expression ')'
        | NOT element
        | function_call_inline
        """
    if len(p) == 2:
        p[0] = AST.ElementNode(p[1])
    elif len(p) == 3:
        # not e
        p[0] = AST.NotNode(p[2])
    else:
        # ( e )
        p[0] = AST.ElementNode(p[2])


# FUNCTION call : inline
def p_function_call_inline(p):
    """ function_call_inline : identifier '(' param_list ')'"""
    p[0] = AST.FunctionCallInlineNode(p[1], p[3])


"""
    TYPE IDENTIFIER
"""


# IDENTIFIER
def p_identifier(P):
    """ identifier : IDENTIFIER """
    P[0] = AST.IDNode(str(P[1]).lower())


"""
    VARIABLE TYPES
"""


# REAL
def p_real(p):
    """ real : REAL """
    p[0] = AST.RealNode(p[1])


# INTEGER
def p_integer(p):
    """ integer : INTEGER """
    p[0] = AST.IntNode(p[1])


# CHAR
def p_char(p):
    """ char : CHAR """
    p[0] = AST.CharNode(p[1])


"""
    ERROR
"""


# ERROR check
def p_error(p):
    print("Syntax error in line %d" % p.lineno)
    parser.errok()


parser = yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys
    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog, debug=1)
    print(result)
