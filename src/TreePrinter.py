from __future__ import print_function
from src import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Basic)
    def printTree(self, indent=0):
        print("| " * indent + str(self.value))

    @addToClass(AST.KeyBasic)
    def printTree(self, indent=0):
        print("| " * indent + self.value.upper())

    @addToClass(AST.KeyBasicExtended)
    def printTree(self, indent=0):
        print("| " * indent + self.value.upper())
        self.expr.printTree(indent + 1)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print("| " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.AssignInstr)
    def printTree(self, indent=0):
        print("| " * indent + self.op)
        print("| " + self.left)
        self.right.printTree(indent + 1)

    @addToClass(AST.Transpose)
    def printTree(self, indent=0):
        print("| " * indent + "TRANSPOSE")
        self.left.printTree(indent + 1)

    @addToClass(AST.RightOneExpr)
    def printTree(self, indent=0):
        print("| " * indent + self.op)
        self.right.printTree(indent + 1)

    @addToClass(AST.MatrixDeclarations)
    def printTree(self, indent=0):
        print("| " * indent + self.key_word)
        self.expr.printTree(indent + 1)

    @addToClass(AST.Doubler)
    def printTree(self, indent=0):
        self.left.printTree(indent)
        self.right.printTree(indent)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        print("| " * indent + "VECTOR")
        self.vector.printTree(indent+1)

    @addToClass(AST.Ref)
    def printTree(self, indent=0):
        print("| " * indent + self.op)
        print("| " * (indent + 1) + "REF")
        print("| " * (indent + 2) + self.id)
        self.indexes.printTree(indent + 2)
        self.expr.printTree(indent + 1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        print("| " * indent + "FOR")
        self.range.printTree(indent + 1)
        self.instr.printTree(indent + 1)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        print("| " * indent + self.id)
        print("| " * indent + "RANGE")
        self.expr1.printTree(indent + 1)
        self.expr2.printTree(indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        print("| " * indent + "WHILE")
        self.expr.printTree(indent + 1)
        self.instr.printTree(indent + 1)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass

