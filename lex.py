import ply.lex as lex

reserved_words = (
    'integer',
    'real',
    'boolean',
    'true',
    'false'
)

tokens = (
    'ADD_OP',
    'MUL_OP',
    'IDENTIFIER',
) + tuple(map(lambda s: s.upper(), reserved_words))

literals = '();='

t_ADD_OP = r'[+-]'
t_MUL_OP = r'[*/]'
"""
Ces expressions régulières ne supporte pas les notations exponentielles
et les déclaration de real du genre 4.0f.
"""
t_REAL = r'\d+\.\d+'
t_INTEGER = r'\d+'


def t_IDENTIFIER(t):
    r'[A-Za-z_]\w*'
    if t.value.lower() in reserved_words:
        t.type = t.value.upper()
    return t


def t_newline(t):
    r'(\n+)'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % repr(t.value[0]))
    t.lexer.skip(1)


t_ignore = ' \t'
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
