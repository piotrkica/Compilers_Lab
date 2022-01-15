from src import AST
from src import SymbolTable
from src.Memory import *
from src.Exceptions import *
from src.visit import *
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
        left = self.visit(node.left)
        right = self.visit(node.right)
        return left + [right]

    @when(AST.If)
    def visit(self, node):
        expr = self.visit(node.expr)
        if expr:
            self.visit(node.instr)

    @when(AST.IfElse)
    def visit(self, node):
        expr = self.visit(node.expr)
        if expr:
            self.visit(node.instr1)
        else:
            self.visit(node.instr2)

    @when(AST.While)
    def visit(self, node):
        while self.visit(node.expr):
            self.visit(node.instr)

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
        print(self.visit(node.expr))

    @when(AST.PrintDoubler)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return str(left) + ' ' + str(right)

    @when(AST.BinExpr)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if node.op == "+":
            return left + right
        elif node.op == "-":
            return left - right
        elif node.op == "*":
            return left * right
        elif node.op == "/":
            return left / right

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
        return node.value

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.String)
    def visit(self, node):
        return node.value

    @when(AST.ID)
    def visit(self, node):
        return Interpreter.memory.get(node.name)

    @when(AST.Error)
    def visit(self, node):
        pass


