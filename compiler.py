import AST
from AST import add_to_class
from functools import reduce

operations = {
    '+' : "ADD\n",
    '-' : "SUB\n",
    '∗' : "MUL\n",
    '/' : "DIV\n",
}

variables = {}

# def whilecounter():
#     whilecounter.current += 1
#     return whilecounter.current
#
# whilecounter.current = 0

@add_to_class(AST.FileNode)
def compile(self):
    bytecode = ""
    for c in self.children:
        bytecode += c.compile()
    return bytecode

@add_to_class(AST.ProgramNode)
def compile(self):
    for c in self.children:
        bytecode += c.compile()
    return bytecode

@add_to_class(AST.VarDeclBlockNode)
def compile(self):
    for c in self.children:
        bytecode += c.compile()
    return bytecode

@add_to_class(AST.VarDeclListNode)
def compile(self):
    for c in self.children:
        bytecode += c.compile()
    return bytecode

@add_to_class(AST.VarDeclarationNode)
def compile(self):
    var_name = self.children[0] # key
    var_type = self.children[1].children[0] # type
    var_value = None

    if variables.has_key(var_name) :
        raise Exeption('symbol', var_name , 'already exist')

    variables[var_name] = (var_type, var_value)

@add_to_class(AST.BlockNode)
def compile(self):
    for c in self.children:
        bytecode += c.compile()
    return bytecode

@add_to_class(AST.StatementListNode)
def compile(self):
    for c in self.children:
        bytecode += c.compile()
    return bytecode


@add_to_class(AST.TokenNode)
def compile(self):
    if isinstance(self.tok, str):
        return "PUSHV %s\n" % self.tok
    else:
        return "PUSHC %s\n" % self.tok

@add_to_class(AST.OpNode)
def compile(self):
    bytecode = ""
    args = [c.compile() for c in self.children]
    for operand in args:
        bytecode += operand
    bytecode += operations[self.op]
    return bytecode

@add_to_class(AST.AssignNode)
def compile(self):
    bytecode = ""
    bytecode += "%s" % self.children[1].compile()
    bytecode += "SET %s\n" % self.children[0].tok
    return bytecode

@add_to_class(AST.PrintNode)
def compile(self):
    bytecode = ""
    bytecode += "%s" % self.children[0].compile()
    bytecode += "PRINT\n"
    return bytecode

# @add_to_class(AST.WhileNode)
# def compile(self):
#     counter = whilecounter()
#     bytecode = ""
#     bytecode += "JMP cond%s\n" % counter
#     bytecode += "body%s:" % counter
#     bytecode += self.children[1].compile()
#     bytecode += "cond%s:" % counter
#     bytecode += self.children[0].compile()
#     bytecode += "JINZ body%s" % counter
#     return bytecode

if __name__ == "__main__":
    from parser import parse
    import sys, os
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    compiled = ast.compile()
    name = os.path.splitext(sys.argv[1])[0] + '.vm'
    outfile = open(name, 'w')
    outfile.write(compiled)
    outfile.close()
    print("Wrote output to", name)
