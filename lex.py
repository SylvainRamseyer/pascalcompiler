import ply.lex as lex

# RESERVED WORDS
reserved_words = (
    'integer',
    'real',
    'char'
)

# LEXEME TYPES definition
# addition : reserved words into tokens
tokens = (
    'ADD_OP',
    'MUL_OP',
    'IDENTIFIER',
) + tuple(map(lambda s: s.upper(), reserved_words))

literals = '();={}'


# LEXEMES : + -
def t_ADD_OP(t):
    r"""[+-]"""
    return t


# LEXEMES : * /
def t_MUL_OP(t):
    r"""[*/^//]"""
    return t


# IDENTIFIER : variables' name
# check : reserved words
def t_IDENTIFIER(t):
    r"""[A-Za-z_]\w*"""
    if t.value in reserved_words:
        t.type = t.value.upper()
    return t


# NUMBERS : returns number
def t_REAL(t):
    r"""\d+\.\d+"""
    return t


def t_INTEGER(t):
    r"""\d+"""
    return t

def t_CHAR(t):
    r"""['].[']|['][']"""
    return t


# LINE NUMBER : in case of error occurrence
def t_newline(t):
    r"""(\n+)"""
    t.lexer.lineno += len(t.value)


# COMMENT : inline  -> Pascal //, multi-line -> Pascal {}
def t_COMMENT(t):
    # r"""(?://[^\n]*|/\*(?:(?!\*/).)*\*/)"""
    r"""\#.*"""
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
