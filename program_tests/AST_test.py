# coding: latin-1

""" Petit module utilitaire pour la construction, la manipulation et la
reprï¿½sentation d'arbres syntaxiques abstraits.

Sï¿½rement plein de bugs et autres surprises. ï¿½ prendre comme un
"work in progress"...
Notamment, l'utilisation de pydot pour reprï¿½senter un arbre syntaxique cousu
est une utilisation un peu "limite" de graphviz. ï¿½a marche, mais le layout n'est
pas toujours optimal...
"""
import pydot


class Node:
    count = 0
    type = 'Node (unspecified)'
    shape = 'ellipse'

    def __init__(self, children=None):
        self.ID = str(Node.count)
        Node.count += 1
        if not children:
            self.children = []
        elif hasattr(children, '__len__'):
            self.children = children
        else:
            self.children = [children]
        self.next = []

    def addNext(self, next):
        self.next.append(next)

    def asciitree(self, prefix=''):
        result = "%s%s\n" % (prefix, repr(self))
        prefix += '|  '
        for c in self.children:
            if not isinstance(c,Node):
                result += "%s*** Error: Child of type %r: %r\n" % (prefix, type(c), c)
                continue
            result += c.asciitree(prefix)
        return result

    def __str__(self):
        return self.asciitree()

    def __repr__(self):
        return self.type

    def makegraphicaltree(self, dot=None, edgeLabels=True):
            if not dot: dot = pydot.Dot()
            dot.add_node(pydot.Node(self.ID,label=repr(self), shape=self.shape))
            label = edgeLabels and len(self.children)-1
            for i, c in enumerate(self.children):
                c.makegraphicaltree(dot, edgeLabels)
                edge = pydot.Edge(self.ID,c.ID)
                if label:
                    edge.set_label(str(i))
                dot.add_edge(edge)
                # Workaround for a bug in pydot 1.0.2 on Windows:
                # dot.set_graphviz_executables({'dot': r'C:\Program Files\Graphviz2.16\bin\dot.exe'})
            return dot
        
    def threadTree(self, graph, seen = None, col=0):
            colors = ('red', 'green', 'blue', 'yellow', 'magenta', 'cyan')
            if not seen: seen = []
            if self in seen: return
            seen.append(self)
            new = not graph.get_node(self.ID)
            if new:
                graphnode = pydot.Node(self.ID,label=repr(self), shape=self.shape)
                graphnode.set_style('dotted')
                graph.add_node(graphnode)
            label = len(self.next)-1
            for i,c in enumerate(self.next):
                if not c: return
                col = (col + 1) % len(colors)
                color = colors[col]
                c.threadTree(graph, seen, col)
                edge = pydot.Edge(self.ID,c.ID)
                edge.set_color(color)
                edge.set_arrowsize('.5')
                # Les arrï¿½tes correspondant aux coutures ne sont pas prises en compte
                # pour le layout du graphe. Ceci permet de garder l'arbre dans sa reprï¿½sentation
                # "standard", mais peut provoquer des surprises pour le trajet parfois un peu
                # tarabiscotï¿½ des coutures...
                # En commantant cette ligne, le layout sera bien meilleur, mais l'arbre nettement
                # moins reconnaissable.
                edge.set_constraint('false')
                if label:
                    edge.set_taillabel(str(i))
                    edge.set_labelfontcolor(color)
                graph.add_edge(edge)
            return graph

"""
    NODE TYPES
"""


# PROGRAM NODE
class ProgramNode(Node):
    type = 'Program'


# TOKEN NODE
class TokenNode(Node):
    type = 'token'

    def __init__(self, tok):
        Node.__init__(self)
        self.tok = tok

    def __repr__(self):
        return repr(self.tok)


# TODO : modification
# OPERATION NODE
class OpNode(Node):
    def __init__(self, op, children):
        Node.__init__(self, children)
        self.op = op
        try:
            self.nbargs = len(children)
        except AttributeError:
            self.nbargs = 1

    def __repr__(self):
        return "%s (%s)" % (self.op, self.nbargs)


# TODO : modification
# ASSIGNMENT NODE
class AssignNode(Node):
    type = '='


# PRINT NODE
class PrintNode(Node):
    type = 'print'


# TODO : modification
# WHILE NODE
class WhileNode(Node):
    type = 'while'


# ENTRY NODE
class EntryNode(Node):
    type = 'ENTRY'

    def __init__(self):
        Node.__init__(self, None)


""""
    NEW NODE TYPES
"""


# BLOCK NODE
class BlockNode(* Node):
    type = 'block'


# VAR LIST NODE

# VAR NODE

# FUNCTION LIST NODE

# FUNCTION HEAD NODE

# FUNCTION CALL NODE

# FUNCTION CALL INLINE NODE

# PROCEDURE NODE

# PROCEDURE HEAD NODE

# PARAMETER NODE

# PARAMETER LIST NODE

# TYPE NODE

# IDENTIFICATION NODE

# STATEMENT LIST NODE

# IF NODE -> THEN -> ELSE

# AND / OR NODE

# NOT NODE

# SIGN NODE

# ELEMENT NODE (token node probably)

# REAL NODE

# INTEGER NODE

# CHAR NODE


"""
    MISC FUNCTION
"""


def addToClass(cls):
    """ Dï¿½corateur permettant d'ajouter la fonction dï¿½corï¿½e en tant que mï¿½thode
    ï¿½ une classe.

    Permet d'implï¿½menter une forme ï¿½lï¿½mentaire de programmation orientï¿½e
    aspects en regroupant les mï¿½thodes de diffï¿½rentes classes implï¿½mentant
    une mï¿½me fonctionnalitï¿½ en un seul endroit.

    Attention, aprï¿½s utilisation de ce dï¿½corateur, la fonction dï¿½corï¿½e reste dans
    le namespace courant. Si cela dï¿½range, on peut utiliser del pour la dï¿½truire.
    Je ne sais pas s'il existe un moyen d'ï¿½viter ce phï¿½nomï¿½ne.
    """
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator
