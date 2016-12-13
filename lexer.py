"""Pascal lexical analyzer."""
import ply.lex as lex

# RESERVED WORDS
reserved_words = (
    'integer',      # variables
    'real',
    'boolean',
    'char',
    'const',
    'var',
    'true',         # boolean
    'false',
    'and',          # logical
    'or',
    'not',
    'program',      # program
    'begin',
    'end',
    'function',
    'procedure',
    'if',           # flow control
    'then',
    'else',
    'repeat',
    'until',
    'while',
    'do',
    'write',        # misc
    'writeln'
)

# LEXEME TYPES definition
# addition : reserved words into tokens
tokens = (
    'ADD_OP',
    'MUL_OP',
    'IDENTIFIER'
) + tuple(map(lambda s: s.upper(), reserved_words))

t_ADD_OP = r'[+-]'              # LEXEMES : + -
t_MUL_OP = r'[*/]'              # LEXEMES : * /
t_INTEGER = r'\d+'              # INTEGER : returns an integer
'''FLOATING NUMBERS: numbers like 4.0f are not handled '''
t_REAL = r'\d+\.\d+'
t_CHAR = r"""['].[']|['][']"""  # CHAR: returns character
t_VAR = r"""(?i)var"""
t_CONST = r"""(?i)const"""
t_AND = r"""(?i)and"""          # LOGICAL OPERATORS
t_OR = r"""(?i)or"""
t_NOT = r"""(?i)not"""
t_IF = r"""(?i)if"""            # FLOW CONTROL
t_THEN = r"""(?i)then"""
t_ELSE = r"""(?i)else"""
t_REPEAT = r"""(?i)repeat"""
t_UNTIL = r"""(?i)until"""
t_WHILE = r"""(?i)while"""
t_DO = r"""(?i)do"""
t_PROGRAM = r"""(?i)program"""  # RESERVED WORDS
t_PROCEDURE = r"""(?i)procedure"""
t_FUNCTION = r"""(?i)function"""
t_BEGIN = r"""(?i)begin"""      # END/START SECTION
t_END = r"""(?i)end"""
t_WRITE = r"""(?i)write"""      # MISC
t_WRITELN = r"""(?i)writeln"""
literals = '();={}.:'


# IDENTIFIER : variables' name
# check : reserved words
def t_IDENTIFIER(t):
    r"""[A-Za-z_]\w*"""
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
    print('''\
   ___          _                 ___                    _     __
  / __\__ _ ___| |_ ___  _ __    / _ \__ _ ___  ___ __ _| |   / /  _____  \
_____ _ __
 / /  / _` / __| __/ _ \| '__|  / /_)/ _` / __|/ __/ _` | |  / /  / _ \ \/ \
/ _ \ '__|
/ /__| (_| \__ \ || (_) | |    / ___/ (_| \__ \ (_| (_| | | / /__|  __/>  \
<  __/ |
\____/\__,_|___/\__\___/|_|    \/    \__,_|___/\___\__,_|_| \____/\___/_/\
\_\___|_|
''')
    while 1:
        tok = lex.token()
        if not tok:
            break
        print("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
