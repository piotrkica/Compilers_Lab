import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *
import sys

sys.setrecursionlimit(10000)


class Interpreter(object):
    memory = MemoryStack(Memory("GlobalMemory"))

    @on('node')
    def visit(self, node):
        pass

    @when(AST.InstructionDoubler)
    def visit(self, node):
        self.visit(node.left)
        self.visit(node.right)

    @when(AST.AssignInstr)
    def visit(self, node):
        if node.op == '=':
            Interpreter.memory.insert(node.left.name, self.visit(node.right))
        else:
            value = Interpreter.memory.get(node.left.name)
            right = self.visit(node.right)
            if node.op == "+=":
                value += right
            elif node.op == "-=":
                value -= right
            elif node.op == "*=":
                value *= right
            elif node.op == "/=":
                value /= right
            Interpreter.memory.set(node.left.name, value)

    @when(AST.AssignInstrVector)
    def visit(self, node):
        pass

    @when(AST.AssignInstrRef)
    def visit(self, node):
        pass

    @when(AST.AssignUnary)
    def visit(self, node):
        pass

    @when(AST.Vector)
    def visit(self, node):
        pass

    @when(AST.SubarrayDoubler)
    def visit(self, node):
        pass

    @when(AST.IndexDoubler)
    def visit(self, node):
        pass

    @when(AST.If)
    def visit(self, node):
        pass

    @when(AST.IfElse)
    def visit(self, node):
        pass

    @when(AST.While)
    def visit(self, node):
        pass

    @when(AST.For)
    def visit(self, node):
        pass

    @when(AST.Range)
    def visit(self, node):
        pass

    @when(AST.Break)
    def visit(self, node):
        pass

    @when(AST.Continue)
    def visit(self, node):
        pass

    @when(AST.Return)
    def visit(self, node):
        pass

    @when(AST.ReturnExpression)
    def visit(self, node):
        pass

    @when(AST.Print)
    def visit(self, node):
        pass

    @when(AST.PrintDoubler)
    def visit(self, node):
        pass

    @when(AST.BinExpr)
    def visit(self, node):
        pass

    @when(AST.MatrixBinExpr)
    def visit(self, node):
        pass

    @when(AST.Transpose)
    def visit(self, node):
        pass

    @when(AST.MatrixDeclarations)
    def visit(self, node):
        pass

    @when(AST.IntNum)
    def visit(self, node):
        pass

    @when(AST.FloatNum)
    def visit(self, node):
        pass

    @when(AST.String)
    def visit(self, node):
        pass

    @when(AST.ID)
    def visit(self, node):
        pass

    @when(AST.Error)
    def visit(self, node):
        pass


