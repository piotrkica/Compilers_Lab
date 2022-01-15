class Node(object):
    def __init__(self, lineno):
        self.lineno = lineno

    def accept(self, visitor):
        visitor.visit(self)


class InstructionDoubler(Node):
    def __init__(self, left, right, lineno):
        self.left = left
        self.right = right
        super().__init__(lineno)


class AssignInstr(Node):
    def __init__(self, op, left, right, lineno):
        self.op = op
        self.left = left
        self.right = right
        super().__init__(lineno)


class AssignInstrVector(Node):
    def __init__(self, op, left, name, indexes, lineno):
        self.op = op
        self.left = left
        self.name = name
        self.indexes = indexes
        super().__init__(lineno)


class AssignInstrRef(Node):
    def __init__(self, op, id, indexes, expr, lineno):
        self.op = op
        self.id = id
        self.indexes = indexes
        self.expr = expr
        super().__init__(lineno)


class AssignUnary(Node):
    def __init__(self, op, id, expr, lineno):
        self.op = op
        self.id = id
        self.expr = expr
        super().__init__(lineno)


class Vector(Node):
    def __init__(self, vector, lineno):
        self.vector = vector
        super().__init__(lineno)


class SubarrayDoubler(Node):
    def __init__(self, left, right, lineno):
        self.left = left
        self.right = right
        super().__init__(lineno)


class IndexDoubler(Node):
    def __init__(self, left, right, lineno):
        self.left = left
        self.right = right
        super().__init__(lineno)


class If(Node):
    def __init__(self, expr, instr, lineno):
        self.expr = expr
        self.instr = instr
        super().__init__(lineno)


class IfElse(Node):
    def __init__(self, expr, instr1, instr2, lineno):
        self.expr = expr
        self.instr1 = instr1
        self.instr2 = instr2
        super().__init__(lineno)


class While(Node):
    def __init__(self, expr, instr, lineno):
        self.expr = expr
        self.instr = instr
        super().__init__(lineno)


class For(Node):
    def __init__(self, range, instr, lineno):
        self.range = range
        self.instr = instr
        super().__init__(lineno)


class Range(Node):
    def __init__(self, id, expr1, expr2, lineno):
        self.id = id
        self.expr1 = expr1
        self.expr2 = expr2
        super().__init__(lineno)


class Break(Node):
    def __init__(self, lineno):
        super().__init__(lineno)


class Continue(Node):
    def __init__(self, lineno):
        super().__init__(lineno)


class Return(Node):
    def __init__(self, lineno):
        super().__init__(lineno)


class ReturnExpression(Node):
    def __init__(self, expr, lineno):
        self.expr = expr
        super().__init__(lineno)


class Print(Node):
    def __init__(self, expr, lineno):
        self.expr = expr
        super().__init__(lineno)


class PrintDoubler(Node):
    def __init__(self, left, right, lineno):
        self.left = left
        self.right = right
        super().__init__(lineno)


class BinExpr(Node):
    def __init__(self, op, left, right, lineno):
        self.op = op
        self.left = left
        self.right = right
        super().__init__(lineno)


class MatrixBinExpr(Node):
    def __init__(self, op, left, right, lineno):
        self.op = op
        self.left = left
        self.right = right
        super().__init__(lineno)


class Transpose(Node):
    def __init__(self, left, lineno):
        self.left = left
        super().__init__(lineno)


class MatrixDeclarations(Node):
    def __init__(self, key_word, indexes, lineno):
        self.key_word = key_word
        self.indexes = indexes
        super().__init__(lineno)


class IntNum(Node):
    def __init__(self, value, lineno):
        self.value = value
        super().__init__(lineno)


class FloatNum(Node):
    def __init__(self, value, lineno):
        self.value = value
        super().__init__(lineno)


class String(Node):
    def __init__(self, value, lineno):
        self.value = value
        super().__init__(lineno)


class ID(Node):
    def __init__(self, name, lineno):
        self.name = name
        super().__init__(lineno)


class Error(Node):
    def __init__(self, lineno):
        super().__init__(lineno)
