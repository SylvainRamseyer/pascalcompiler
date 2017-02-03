"""
AST module.

Petit module utilitaire pour la construction, la manipulation et la
représentation d'arbres syntaxiques abstraits.

Sûrement plein de bugs et autres surprises. À prendre comme un
"work in progress"...
Notamment, l'utilisation de pydot pour représenter un arbre syntaxique cousu
est une utilisation un peu "limite" de graphviz. ça marche, mais le layout
n'est pas toujours optimal...
"""

import pydot


class Node:
    """Class representing an AST node."""

    count = 0
    type = 'Node (unspecified)'
    shape = 'ellipse'

    def __init__(self, children=None):
        """
        Constructor.

        Children agrument is a list containg children of the current node.
        """
        self.ID = str(Node.count)
        Node.count += 1
        if not children:
            self.children = []
        elif hasattr(children, '__len__'):
            self.children = children
        else:
            self.children = [children]
        self.next = []

    def add_next(self, next):
        """Adds a node to the current node."""
        self.next.append(next)

    def ascii_tree(self, prefix=''):
        """Returns the ASCII tree for console displaying."""
        result = "%s%s\n" % (prefix, repr(self))
        prefix += '|  '
        for c in self.children:
            if not isinstance(c, Node):
                result += "%s*** Error: Child of type %r: %r\n" % (
                    prefix, type(c), c
                )
                continue
            result += c.ascii_tree(prefix)
        return result

    def __str__(self):
        """Returns the node's string reprensentation."""
        return self.ascii_tree()

    def __repr__(self):
        return self.type

    def make_graphical_tree(self, dot=None, edge_labels=True):
            if not dot:
                dot = pydot.Dot()
            dot.add_node(
                pydot.Node(self.ID, label=repr(self), shape=self.shape)
            )
            label = edge_labels and len(self.children) - 1
            for i, c in enumerate(self.children):
                c.make_graphical_tree(dot, edge_labels)
                edge = pydot.Edge(self.ID, c.ID)
                if label:
                    edge.set_label(str(i))
                dot.add_edge(edge)
                # Workaround for a bug in pydot 1.0.2 on Windows:
                # dot.set_graphviz_executables({
                #   'dot': r'C:\Program Files\Graphviz2.16\bin\dot.exe'
                # })
            return dot

    def thread_tree(self, graph, seen=None, col=0):
            colors = ('red', 'green', 'blue', 'yellow', 'magenta', 'cyan')
            if not seen:
                seen = []
            if self in seen:
                return
            seen.append(self)
            new = not graph.get_node(self.ID)
            if new:
                graph_node = pydot.Node(
                    self.ID, label=repr(self), shape=self.shape
                )
                graph_node.set_style('dotted')
                graph.add_node(graph_node)
            label = len(self.next)-1
            for i, c in enumerate(self.next):
                if not c:
                    return
                col = (col + 1) % len(colors)
                color = colors[col]
                c.thread_tree(graph, seen, col)
                edge = pydot.Edge(self.ID, c.ID)
                edge.set_color(color)
                edge.set_arrowsize('.5')
                # Les arrètes correspondant aux coutures ne sont pas prises en
                # compte pour le layout du graphe. Ceci permet de garder
                # l'arbre dans sa représentation "standard", mais peut
                # provoquer des surprises pour le trajet parfois un peu
                # tarabiscoté des coutures... En commantant cette ligne, le
                # layout sera bien meilleur, mais l'arbre nettement moins
                # reconnaissable.
                edge.set_constraint('false')
                if label:
                    edge.set_taillabel(str(i))
                    edge.set_labelfontcolor(color)
                graph.add_edge(edge)
            return graph


"""
    NODE TYPES
"""


class FileNode(Node):
    type = 'File'


# PROGRAM
class ProgramNode(Node):
    type = 'Program'

    def __init__(self, program_indentifier, children):
        Node.__init__(self, children)
        self.program_indentifier = program_indentifier

    def __repr__(self):
        return repr(self.program_indentifier)


class VarDeclBlockNode(Node):
    type = "var_decl_block"


class VarDeclListNode(Node):
    type = "var_decl_list"


class VarDeclarationNode(Node):
    type = "var_declaration"


class TypeNode(Node):
    type = "type"


# TOKEN
class TokenNode(Node):
    type = 'token'

    def __init__(self, tok):
        Node.__init__(self)
        self.tok = tok

    def __repr__(self):
        return repr(self.tok)


# OPERATION
class OpNode(Node):
    def __init__(self, op, children):
        Node.__init__(self, children)
        self.op = op
        try:
            self.args_number = len(children)
        except AttributeError:
            self.args_number = 1

    def __repr__(self):
        return "%s (%s)" % (self.op, self.args_number)


# ASSIGNATION
class AssignNode(Node):
    type = '='


# BLOCK
class StatementListNode(Node):
    type = 'statement_list'


# BLOCK
class BlockNode(Node):
    type = 'block'


# PRINT
class PrintNode(Node):
    type = 'print'


# WHILE
class WhileNode(Node):
    type = 'while'


# ENTRY
class EntryNode(Node):
    type = 'ENTRY'

    def __init__(self):
        Node.__init__(self, None)


# DECORATOR
def add_to_class(cls):
    """ Décorateur permettant d'ajouter la fonction décorée en tant que méthode
    à une classe.

    Permet d'implémenter une forme élémentaire de programmation orientée
    aspects en regroupant les méthodes de différentes classes implémentant
    une même fonctionnalité en un seul endroit.

    Attention, après utilisation de ce décorateur, la fonction décorée reste
    dans le namespace courant. Si cela dérange, on peut utiliser del pour la
    détruire. Je ne sais pas s'il existe un moyen d'éviter ce phénomène.
    """
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator
