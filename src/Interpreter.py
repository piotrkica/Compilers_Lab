from src import AST
from src import SymbolTable
from src.Memory import *
from src.Exceptions import *
from src.visit import *
import sys
import copy

sys.setrecursionlimit(10000)


class Interpreter(object):
    memory = MemoryStack(Memory("GlobalMemory"))  # TODO taka pamiec?

    @on('node')
    def visit(self, node):
        pass

    @when(AST.InstructionDoubler)  # TODO self.visit vs self.accept
    def visit(self, node):
        self.visit(node.left)
        self.visit(node.right)

    @when(AST.AssignInstr)
    def visit(self, node):
        if node.op == '=':
            if Interpreter.memory.get(node.left.name) is None:
                Interpreter.memory.insert(node.left.name, self.visit(node.right))
            else:
                Interpreter.memory.set(node.left.name, self.visit(node.right))
        else:
            value = Interpreter.memory.get(node.left.name)
            right = self.visit(node.right)
            if node.op == "+=":  # TODO poprawic
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
            if Interpreter.memory.get(node.left.name) is None:
                Interpreter.memory.insert(node.left.name, self.visit(node.right))
            else:
                Interpreter.memory.set(node.left.name, self.visit(node.right))
        else:
            value = Interpreter.memory.get(node.left.name)
            right = self.visit(node.right)
            if node.op == "+=":  # TODO poprawic
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
        (T, indexex) = self.visit(node.ref)
        indexes = [[]]
        while len(indexex) > 0:
            tmp = []
            for list_index in indexes:
                if isinstance(indexex[-1], tuple):
                    (start, stop) = indexex[-1]
                    for i in range(start, stop):
                        tmp.append(list_index + [i])
                else:
                    tmp.append(list_index + [indexex[-1]])
            indexex.pop()
            indexes = tmp
        value = self.visit(node.expr)
        for list_index in indexes:
            T = Interpreter.memory.get(node.ref.id.name)
            while len(list_index) > 1:
                T = T[list_index[-1]]
                list_index.pop()
            if node.op == "=":  # TODO poprawic
                T[list_index[-1]] = value
            elif node.op == "+=":
                T[list_index[-1]] += value
            elif node.op == "-=":
                T[list_index[-1]] -= value
            elif node.op == "*=":
                T[list_index[-1]] *= value
            elif node.op == "/=":
                T[list_index[-1]] /= value

    @when(AST.ArrayRef)
    def visit(self, node):
        indexes = self.visit(node.indexes)
        T = Interpreter.memory.get(node.id.name)
        return (T, indexes)

    @when(AST.AssignUnary)
    def visit(self, node):
        if Interpreter.memory.get(node.id.name) is None:
            Interpreter.memory.insert(node.id.name, -self.visit(node.expr))
        else:
            Interpreter.memory.set(node.id.name, -self.visit(node.expr))

    @when(AST.Vector)
    def visit(self, node):
        return self.visit(node.vector)

    @when(AST.SubarrayDoubler)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if isinstance(node.left, AST.SubarrayDoubler):
            arrays = left + [right]
        else:
            arrays = [left] + [right]
        return arrays

    @when(AST.IndexDoubler)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if isinstance(left, list):
            indexes = left + [right]
        else:
            indexes = [left] + [right]
        return indexes

    @when(AST.IndexRange)
    def visit(self, node):
        start = self.visit(node.left)
        stop = self.visit(node.right)
        return (start, stop)

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
        Interpreter.memory.push(Memory("For"))
        (name, start, stop) = self.visit(node.range)
        for _ in range(start, stop):  # TODO moze na while z pozwoleniem modyfikacji zmiennej sterujacej
            self.visit(node.instr)
            Interpreter.memory.set(name, Interpreter.memory.get(name)+1)
        Interpreter.memory.pop()

    @when(AST.Range)
    def visit(self, node):
        start = self.visit(node.expr1)
        stop = self.visit(node.expr2)
        Interpreter.memory.insert(node.id.name, start)
        return (node.id.name, start, stop)

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
        if isinstance(self.visit(node.expr), tuple):
            (T, indexes) = self.visit(node.expr)
            while len(indexes) > 0:
                T = T[indexes[-1]]
                indexes.pop()
            print(T)
        else:
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
        if node.op == "+":  # TODO poprawic
            return left + right
        elif node.op == "-":
            return left - right
        elif node.op == "*":
            return left * right
        elif node.op == "/":
            return left / right
        elif node.op == "<":
            return left < right
        elif node.op == ">":
            return left > right
        elif node.op == "<=":
            return left <= right
        elif node.op == ">=":
            return left >= right
        elif node.op == "!=":
            return left != right
        elif node.op == "==":
            return left == right

    @when(AST.MatrixBinExpr)  # TODO tylko dla 2
    def visit(self, node):
        L = self.visit(node.left)
        R = self.visit(node.right)
        tmp = copy.deepcopy(L)
        for i in range(len(L)):
            for j in range(len(L[0])):
                if node.op == ".+":  # TODO poprawic
                    tmp[i][j] = L[i][j] + R[i][j]
                elif node.op == ".-":
                    tmp[i][j] = L[i][j] - R[i][j]
                elif node.op == ".*":
                    tmp[i][j] = L[i][j] * R[i][j]
                elif node.op == "./":
                    tmp[i][j] = L[i][j] / R[i][j]
        return tmp

    @when(AST.Transpose)  # TODO tylko dla 2
    def visit(self, node):
        M = Interpreter.memory.get(node.left.name)
        rows = len(M)
        cols = len(M[0])
        T = [[0 for _ in range(rows)] for _ in range(cols)]
        for i in range(rows):
            for j in range(cols):
                T[j][i] = M[i][j]
        return T

    @when(AST.MatrixDeclarations)
    def visit(self, node):  # TODO eye do wymiaru 2
        indexes = self.visit(node.indexes)
        T = None
        if isinstance(indexes, int):
            if node.key_word == "eye":
                T = [[0 for _ in range(indexes)] for _ in range(indexes)]
                for i in range(indexes):
                    T[i][i] = 1
            elif node.key_word == "ones":
                T = [[1 for _ in range(indexes)] for _ in range(indexes)]
            elif node.key_word == "zeros":
                T = [[0 for _ in range(indexes)] for _ in range(indexes)]
        else:
            indexes = list(reversed(indexes))
            if node.key_word == "eye":
                T = [[0 for _ in range(indexes[0])] for _ in range(indexes[1])]
                for i in range(min(indexes[0], indexes[1])):
                    T[i][i] = 1
            elif node.key_word == "ones":
                T = 1
                for size in indexes:
                    tmp = []
                    for _ in range(size):
                        tmp.append(copy.deepcopy(T))
                    T = copy.deepcopy(tmp)
            elif node.key_word == "zeros":
                T = 0
                for size in indexes:
                    tmp = []
                    for _ in range(size):
                        tmp.append(copy.deepcopy(T))
                    T = copy.deepcopy(tmp)
        return T

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


