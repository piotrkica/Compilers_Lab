class Node(object):
    pass


class InstructionDoubler(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class AssignInstr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class AssignInstrRef(Node):
    def __init__(self, op, id, indexes, expr):
        self.op = op
        self.id = id
        self.indexes = indexes
        self.expr = expr


class Vector(Node):
    def __init__(self, vector):
        self.vector = vector


class SubarrayDoubler(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class IndexDoubler(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class If(Node):
    def __init__(self, expr, instr):
        self.expr = expr
        self.instr = instr


class IfElse(Node):
    def __init__(self, expr, instr1, instr2):
        self.expr = expr
        self.instr1 = instr1
        self.instr2 = instr2


class While(Node):
    def __init__(self, expr, instr):
        self.expr = expr
        self.instr = instr


class For(Node):
    def __init__(self, range, instr):
        self.range = range
        self.instr = instr


class Range(Node):
    def __init__(self, id, expr1, expr2):
        self.id = id
        self.expr1 = expr1
        self.expr2 = expr2


class Break(Node):
    def __init__(self, value):
        self.value = value


class Continue(Node):
    def __init__(self, value):
        self.value = value


class Return(Node):
    def __init__(self, value):
        self.value = value


class ReturnExpression(Node):
    def __init__(self, value, expr):
        self.value = value
        self.expr = expr


class Print(Node):
    def __init__(self, value, expr):
        self.value = value
        self.expr = expr


class PrintDoubler(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class MatrixBinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Transpose(Node):
    def __init__(self, left):
        self.left = left


class MatrixDeclarations(Node):
    def __init__(self, key_word, expr):
        self.key_word = key_word
        self.expr = expr


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class String(Node):
    def __init__(self, value):
        self.value = value


class ID(Node):
    def __init__(self, value):
        self.value = value


class Error(Node):
    def __init__(self):
        pass
