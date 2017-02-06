import AST
from AST import add_to_class
from functools import reduce
import re
from terminal_format import bcolors, print_error_message

operations = {
    '+': "ADD\n",
    '-': "SUB\n",
    '*': "MUL\n",
    '/': "DIV\n",
}

variables = {}

char_pattern = re.compile("'[a-zA-Z]'")
id_pattern = re.compile('[A-Za-z_]\w*')


def whilecounter():
    whilecounter.current += 1
    return whilecounter.current

whilecounter.current = 0


def check_type(val1, val2):
    return type(val1) != type(val2)


@add_to_class(AST.FileNode)
def compile(self):
    bytecode = ""
    for c in self.children:
        bytecode += c.compile()
    return bytecode


@add_to_class(AST.ProgramNode)
def compile(self):
    bytecode = ""
    for c in self.children:
        bytecode += c.compile()
    return bytecode


@add_to_class(AST.VarDeclBlockNode)
def compile(self):
    bytecode = ""
    for c in self.children:
        bytecode += c.compile()
    return bytecode


@add_to_class(AST.VarDeclListNode)
def compile(self):
    bytecode = ""
    for c in self.children:
        bytecode += c.compile()
    return bytecode


@add_to_class(AST.VarDeclarationNode)
def compile(self):
    bytecode = ""
    var_name = self.children[0].tok  # key

    if var_name in variables:
        print_error_message("Variable '{}' already declared".format(
            var_name
            )
        )
        exit()
    variables[var_name] = None
    bytecode += "PUSHC None\n"
    bytecode += "SET %s\n" % self.children[0].tok
    return bytecode


@add_to_class(AST.BlockNode)
def compile(self):
    bytecode = ""
    for c in self.children:
        bytecode += c.compile()
    return bytecode


@add_to_class(AST.StatementListNode)
def compile(self):
    bytecode = ""
    for c in self.children:
        bytecode += c.compile()
    return bytecode


@add_to_class(AST.TokenNode)
def compile(self):
    if isinstance(self.tok, str):
        if self.tok in variables:
            return "PUSHV %s\n" % self.tok
        elif char_pattern.match(self.tok):
            return "PUSHC %s\n" % self.tok
        else:
            print(self.tok)
            print_error_message("Variable '{}' has not been declared.".format(
                self.tok
                )
            )
            exit()
    else:
        if id_pattern.match(str(self.tok).replace("'", "")):
            print("Truc chelou")
            return "PUSHV %s\n" % str(self.tok).rstrip('\n').replace("'", "")
        return "PUSHC %s\n" % str(self.tok).rstrip('\n').replace("'", "")


@add_to_class(AST.OpNode)
def compile(self):
    bytecode = ""
    args = [c.compile() for c in self.children]

    if len(args) == 1:
        bytecode += "PUSHC %s" % self.children[0]
        return bytecode + "USUB %s" % self.children[0]

    for operand in args:
        bytecode += operand
    bytecode += operations[self.op]
    return bytecode


@add_to_class(AST.AssignNode)
def compile(self):
    bytecode = ""
    bytecode += "%s" % self.children[1].compile()
    if self.children[0].tok not in variables:
        print_error_message("Variable '{}' has not been declared.".format(
            self.children[0].tok
            )
        )
        exit()
    bytecode += "SET %s\n" % self.children[0].tok
    return bytecode


@add_to_class(AST.PrintNode)
def compile(self):
    bytecode = ""
    bytecode += "%s" % self.children[0].compile()
    bytecode += "PRINT\n"
    return bytecode


@add_to_class(AST.BoolExpressionNode)
def compile(self, counter):
    bytecode = ""
    for child in self.children:
        bytecode += child.compile()

    if self.op == '<>':
        bytecode += "SUB\n"
        bytecode += "JINZ body%s\n" % counter
    return bytecode


@add_to_class(AST.WhileNode)
def compile(self):
    counter = whilecounter()
    bytecode = ""
    bytecode += "JMP cond%s\n" % counter
    bytecode += "body%s: " % counter
    bytecode += self.children[1].compile()
    bytecode += "cond%s: " % counter
    bytecode += self.children[0].compile(counter)
    return bytecode


def print_banner():
    print("""\

  /$$$$$$                                    /$$ /$$
 /$$__  $$                                  |__/| $$
| $$  \__/  /$$$$$$  /$$$$$$/$$$$   /$$$$$$  /$$| $$  /$$$$$$   /$$$$$$
| $$       /$$__  $$| $$_  $$_  $$ /$$__  $$| $$| $$ /$$__  $$ /$$__  $$
| $$      | $$  \ $$| $$ \ $$ \ $$| $$  \ $$| $$| $$| $$$$$$$$| $$  \__/
| $$    $$| $$  | $$| $$ | $$ | $$| $$  | $$| $$| $$| $$_____/| $$
|  $$$$$$/|  $$$$$$/| $$ | $$ | $$| $$$$$$$/| $$| $$|  $$$$$$$| $$
 \______/  \______/ |__/ |__/ |__/| $$____/ |__/|__/ \_______/|__/
                                  | $$
                                  | $$
                                  |__/
""")

if __name__ == "__main__":
    from pascal_parser import parse
    import sys
    import os
    print_banner()
    prog = open(sys.argv[1]).read()
    try:
        ast = parse(prog)
    except Exception as e:
        exit(e)
    compiled = ast.compile()
    name = os.path.splitext(sys.argv[1])[0] + '.vm'
    outfile = open(name, 'w')
    outfile.write(compiled)
    outfile.close()
    print("Wrote output to", name)
