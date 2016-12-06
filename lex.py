import ply.lex as lex

# RESERVED WORDS
reserved_words = (
    'integer',
    'real',
    'boolean',
    'true',
    'false',
    'char',
    'and',
    'or',
    'not',
    'begin',
    'end'
)

# LEXEME TYPES definition
# addition : reserved words into tokens
tokens = (
    'ADD_OP',
    'MUL_OP',
    'IDENTIFIER',
) + tuple(map(lambda s: s.upper(), reserved_words))

t_ADD_OP = r'[+-]'  # LEXEMES : + -
t_MUL_OP = r'[*/]'  # LEXEMES : * /
"""
Ces expressions régulières ne supporte pas les notations exponentielles
et les déclaration de real du genre 4.0f.
"""
t_REAL = r'\d+\.\d+'            # NUMBERS : returns number
t_INTEGER = r'\d+'
t_CHAR = r"""['].[']|['][']"""  # CHAR: returns character
t_AND = r"""(?i)and"""     # LOGICAL OPERATORS
t_OR = r"""(?i)or"""
t_NOT = r"""(?i)not"""
literals = '();={}.'


# IDENTIFIER : variables' name
# check : reserved words
def t_IDENTIFIER(t):
    r'[A-Za-z_]\w*'
    if t.value.lower() in reserved_words:
        t.type = t.value.upper()
    return t


# LINE NUMBER : in case of error occurrence
def t_newline(t):
    r"""(\n+)"""
    t.lexer.lineno += len(t.value)


# COMMENT : inline  -> Pascal //, multi-line -> Pascal {}
def t_COMMENT(t):
    r"""{(.|[\r\n])*}"""
    pass


# ERROR GENERATOR : in case of unexpected error occurrence
def t_error(t):
    print("Illegal character '%s'" % repr(t.value[0]))
    t.lexer.skip(1)


# IGNORE : spaces + tabs
t_ignore = ' \t'
# building lexer
lex.lex()

if __name__ == "__main__":
    import sys
    prog = open(sys.argv[1]).read()

    lex.input(prog)

    while 1:
        tok = lex.token()
        if not tok:
            break
        print("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
