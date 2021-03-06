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

    @addToClass(AST.InstructionDoubler)
    def printTree(self, indent=0):
        self.left.printTree(indent)
        self.right.printTree(indent)

    @addToClass(AST.AssignInstr)
    def printTree(self, indent=0):
        print("| " * indent + self.op)
        print("| " * (indent + 1) + self.left.name)
        self.right.printTree(indent + 1)

    @addToClass(AST.AssignInstrVector)
    def printTree(self, indent=0):
        print("| " * indent + self.op)
        self.indexes.printTree(indent + 1)

    @addToClass(AST.AssignInstrRef)
    def printTree(self, indent=0):
        print("| " * indent + self.op)
        self.ref.printTree(indent + 1)
        self.expr.printTree(indent + 1)

    @addToClass(AST.ArrayRef)
    def printTree(self, indent=0):
        print("| " * indent + "REF")
        print("| " * (indent + 1) + self.id.name)
        self.indexes.printTree(indent + 1)

    @addToClass(AST.AssignUnary)
    def printTree(self, indent=0):
        print("| " * indent + self.op)
        print("| " * (indent + 1) + self.id.name)
        print("| " * (indent + 2) + '-')
        self.expr.printTree(indent + 2)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        print("| " * indent + "VECTOR")
        self.vector.printTree(indent + 1)

    @addToClass(AST.SubarrayDoubler)
    def printTree(self, indent=0):
        self.left.printTree(indent)
        self.right.printTree(indent)

    @addToClass(AST.IndexDoubler)
    def printTree(self, indent=0):
        self.left.printTree(indent)
        self.right.printTree(indent)

    @addToClass(AST.IndexRange)
    def printTree(self, indent=0):
        print("| " * indent + ":")
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.If)
    def printTree(self, indent=0):
        print("| " * indent + "IF")
        self.expr.printTree(indent + 1)
        print("| " * indent + "THEN")
        self.instr.printTree(indent + 1)

    @addToClass(AST.IfElse)
    def printTree(self, indent=0):
        print("| " * indent + "IF")
        self.expr.printTree(indent + 1)
        print("| " * indent + "THEN")
        self.instr1.printTree(indent + 1)
        print("| " * indent + "ELSE")
        self.instr2.printTree(indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        print("| " * indent + "WHILE")
        self.expr.printTree(indent + 1)
        self.instr.printTree(indent + 1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        print("| " * indent + "FOR")
        self.range.printTree(indent + 1)
        self.instr.printTree(indent + 1)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        print("| " * indent + self.id.name)
        print("| " * indent + "RANGE")
        self.expr1.printTree(indent + 1)
        self.expr2.printTree(indent + 1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        print("| " * indent + "BREAK")

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        print("| " * indent + "CONTINUE")

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        print("| " * indent + "RETURN")

    @addToClass(AST.ReturnExpression)
    def printTree(self, indent=0):
        print("| " * indent + "RETURN")
        self.expr.printTree(indent + 1)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        print("| " * indent + "PRINT")
        self.expr.printTree(indent + 1)

    @addToClass(AST.PrintDoubler)
    def printTree(self, indent=0):
        self.left.printTree(indent)
        self.right.printTree(indent)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print("| " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.MatrixBinExpr)
    def printTree(self, indent=0):
        print("| " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Transpose)
    def printTree(self, indent=0):
        print("| " * indent + "TRANSPOSE")
        self.left.printTree(indent + 1)

    @addToClass(AST.MatrixDeclarations)
    def printTree(self, indent=0):
        print("| " * indent + self.key_word)
        self.indexes.printTree(indent + 1)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print("| " * indent + str(self.value))

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print("| " * indent + str(self.value))

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print("| " * indent + self.value)

    @addToClass(AST.ID)
    def printTree(self, indent=0):
        print("| " * indent + self.name)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass
