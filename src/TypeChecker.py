from collections import defaultdict
from dataclasses import dataclass

from src import AST
from src.SymbolTable import SymbolTable

type_map = defaultdict(
    lambda: defaultdict(
        lambda: defaultdict(
            lambda: 'any')))

for oper in ['+', '-', '*', '/', "+=", "-=", "*=", "/="]:
    type_map[oper]["int"]["int"] = "int"
    type_map[oper]["int"]["float"] = "float"
    type_map[oper]["float"]["int"] = "float"
    type_map[oper]["float"]["float"] = "float"

for oper in ['>', '>=', '==', "!=", '<=', "<"]:
    type_map[oper]["int"]["int"] = "bool"
    type_map[oper]["int"]["float"] = "bool"
    type_map[oper]["float"]["int"] = "bool"
    type_map[oper]["float"]["float"] = "bool"

for oper in ['==', "!="]:
    type_map[oper]["str"]["str"] = "bool"

type_map["+"]["str"]["str"] = "str"


@dataclass
class Array:
    size: any
    elem_type: any
    dims: any

    def __hash__(self):
        return hash((self.size, self.elem_type, self.dims))


class NodeVisitor(object):
    symbol_table = SymbolTable(None, 'init')
    loop_depth = 0
    errors = []

    def print_errors(self):
        for error in self.errors:
            print(error)

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):
    def visit_InstructionDoubler(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_AssignInstr(self, node):
        type_right = self.visit(node.right)
        if node.op == "=":
            if type_right == 'any':
                self.errors.append(f"Wrong type in assignment: line={node.lineno}")
            elif type_right is None:
                self.errors.append(f"Missing right side symbol in assignment: line={node.lineno}")
            else:
                self.symbol_table.put(node.left.value, type_right)
        else:
            if node.left.value not in self.symbol_table.symbols:
                self.errors.append(f"Missing symbol in line {node.lineno}")
            else:
                type_left = self.symbol_table.get(node.left.value)
                new_type = type_map[node.op][type_left][type_right]
                if new_type != 'any':
                    self.symbol_table[node.left.value] = new_type
                else:
                    self.errors.append(f"Wrong new type after assignment: line={node.lineno}")

    def visit_AssignInstrVector(self, node):
        type_indexes = self.visit(node.indexes)
        if type_indexes != "int":  # check if this is array of ints
            self.errors.append(f"Wrong index type: line={node.lineno}")
        else:
            size = 1
            tmp_node = node.indexes
            while isinstance(tmp_node, AST.IndexDoubler):
                size += 1
                tmp_node = tmp_node.left
            if node.name.value not in self.symbol_table.symbols:  # check if id was declared
                self.errors.append(f"Missing symbol: line={node.lineno}")
            elif size < self.symbol_table[node.name.value].dims:
                self.errors.append(f"Not enough indexes in reference: line={node.lineno}")
            elif size > self.symbol_table[node.name.value].dims:
                self.errors.append(f"Too many indexes in reference: line={node.lineno}")
            else:
                tmp_node = node.indexes
                tmp_array = self.symbol_table[node.name.value]
                while size > 1:
                    if tmp_node.right.value >= tmp_array.size:
                        self.errors.append(f"Index out of range: line={node.lineno}")
                    tmp_node = tmp_node.left
                    tmp_array = tmp_array.elem_type
                    size -= 1
                if tmp_node.value >= tmp_array.size:
                    self.errors.append(f"Index out of range: line={node.lineno}")

    def visit_AssignInstrRef(self, node):
        type_right = self.visit(node.expr)
        if node.id.value not in self.symbol_table.symbols:  # check if id was declared
            self.errors.append(f"Missing symbol: line={node.lineno}")
        elif not isinstance(self.symbol_table[node.id.value], Array):  # check if it is an array
            self.errors.append(f"Wrong reference object: line={node.lineno}")
        else:
            type_indexes = self.visit(node.indexes)
            if type_indexes != "int":  # check if this is array of ints
                self.errors.append(f"Wrong index type: line={node.lineno}")
            else:
                if isinstance(node.indexes, AST.IntNum):  # edge case for single index
                    indexes_list = [node.indexes.value]
                elif isinstance(node.indexes, AST.IndexDoubler):  # case for multiple indexes
                    indexes_list = []  # list of indexes
                    curr_index = node.indexes
                    while isinstance(curr_index, AST.IndexDoubler):
                        indexes_list.append(curr_index.right.value)
                        curr_index = curr_index.left
                        if not isinstance(curr_index, AST.IndexDoubler):
                            indexes_list.append(curr_index.value)
                    indexes_list = indexes_list[::-1]  # left-recursion in IndexDouble -> reverse
                else:
                    self.errors.append(f"Wrong reference type: line={node.lineno}")
                    return
                type_array = self.symbol_table[node.id.value]
                array_sizes = [type_array.size]
                while isinstance(type_array.elem_type, Array):  # get array sizes down the matrix to compare
                    type_array = type_array.elem_type
                    array_sizes.append(type_array.size)

                if len(indexes_list) > len(array_sizes):  # check if not too many indexes
                    self.errors.append(f"Too many indexes in reference: line={node.lineno}")
                    return
                for i, idx in enumerate(indexes_list):  # compare indexes and array sizes
                    if idx >= array_sizes[i]:
                        self.errors.append(f"Index out of range: line={node.lineno}")
                        return

    def visit_AssignUnary(self, node):
        type_expr = self.visit(node.expr)
        if type_expr not in ["int", "float"]:
            self.errors.append(f"Wrong type in unary assignment: line={node.lineno}")
        self.symbol_table.put(node.id.value, type_expr)

    def visit_Vector(self, node):
        if isinstance(node.vector, AST.IndexDoubler):
            self.visit(node.vector)
            size = 1
            tmp_node = node.vector
            while isinstance(tmp_node, AST.IndexDoubler):
                size += 1
                tmp_node = tmp_node.left
            return Array(size, "int", 1)
        elif isinstance(node.vector, AST.SubarrayDoubler):
            type_doubler = self.visit(node.vector)
            size = 1
            tmp_node = node.vector
            while isinstance(tmp_node, AST.SubarrayDoubler):
                size += 1
                tmp_node = tmp_node.left
            return Array(size, type_doubler, type_doubler.dims + 1)
        elif isinstance(node.vector, AST.Vector):
            type_vector = self.visit(node.vector)
            return Array(1, type_vector, type_vector.dims + 1)
        return "Vector"

    def visit_SubarrayDoubler(self, node):
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)
        if type_left.size != type_right.size:
            self.errors.append(f"Mismatched sizes in matrix declaration in line: {node.lineno}")
        if type_left.dims != type_right.dims:
            self.errors.append(f"Mismatched dimensions in matrix declaration in line: {node.lineno}")

        return Array(type_right.size, "int", type_right.dims)

    def visit_IndexDoubler(self, node):
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)
        if type_left != "int" or type_right != "int":
            self.errors.append(f"Wrong index type: line={node.lineno}")
            print(f"Wrong index type: line={node.lineno}")
        return "int"

    def visit_If(self, node):
        self.visit(node.expr)
        self.symbol_table = self.symbol_table.pushScope("If")
        self.visit(node.instr)
        self.symbol_table = self.symbol_table.popScope()

    def visit_IfElse(self, node):
        self.visit(node.expr)

        self.symbol_table = self.symbol_table.pushScope("If")
        self.visit(node.instr1)
        self.symbol_table = self.symbol_table.popScope()

        self.symbol_table = self.symbol_table.pushScope("Else")
        self.visit(node.instr2)
        self.symbol_table = self.symbol_table.popScope()

    def visit_While(self, node):
        self.loop_depth += 1
        self.symbol_table = self.symbol_table.pushScope("While")
        self.visit(node.expr)
        self.visit(node.instr)
        self.symbol_table = self.symbol_table.popScope()
        self.loop_depth -= 1

    def visit_For(self, node):
        self.loop_depth += 1
        self.symbol_table = self.symbol_table.pushScope("For")
        self.visit(node.range)
        self.visit(node.instr)
        self.symbol_table = self.symbol_table.popScope()
        self.loop_depth -= 1

    def visit_Range(self, node):
        type_expr1 = self.visit(node.expr1)
        type_expr2 = self.visit(node.expr2)
        if type_expr1 != "int" or type_expr2 != "int":
            self.errors.append(f"Wrong type in range: line={node.lineno}")

    def visit_Break(self, node):
        if self.loop_depth <= 0:
            self.errors.append(f"Break usage outside loop: line={node.lineno}")

    def visit_Continue(self, node):
        if self.loop_depth <= 0:
            self.errors.append(f"Continue usage outside loop: line={node.lineno}")

    def visit_Return(self, node):
        pass

    def visit_ReturnExpression(self, node):
        self.visit(node.expr)

    def visit_Print(self, node):
        self.visit(node.expr)

    def visit_PrintDoubler(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_BinExpr(self, node):
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)
        return type_map[node.op][type_left][type_right]

    def visit_MatrixBinExpr(self, node):
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)
        if type_left.dims != type_right.dims:
            self.errors.append(f"Mismatched dimensions in matrix BinExpr in line: {node.lineno}")
        if type_left.elem_type != type_right.elem_type:
            self.errors.append(f"Mismatched submatrices' sizes in matrix BinExpr in line: {node.lineno}")
        if type_left.size != type_right.size:
            self.errors.append(f"Mismatched sizes in matrix BinExpr in line: {node.lineno}")

        return type_left

    def visit_Transpose(self, node):
        self.visit(node.left)
        if node.left.value not in self.symbol_table.symbols:
            self.errors.append(f"Missing matrix to transpose in scope: line={node.lineno}")
            return None
        return self.symbol_table[node.left.value]

    def visit_MatrixDeclarations(self, node):
        type_indexes = self.visit(node.indexes)
        if type_indexes != "int":
            self.errors.append(f"Wrong type in matrix declaration - not an int: line={node.lineno}")
        else:
            indexes = node.indexes
            if isinstance(indexes, AST.IntNum):
                size = indexes.value
                return Array(size, Array(size, "int", 1), 2)
            else:
                array = "int"
                dim = 1
                while isinstance(indexes, AST.IndexDoubler):
                    array = Array(indexes.right.value, array, dim)
                    dim += 1
                    indexes = indexes.left
                return Array(indexes.value, array, dim)
        return "any"

    def visit_IntNum(self, node):
        return "int"

    def visit_FloatNum(self, node):
        return "float"

    def visit_String(self, node):
        return "str"

    def visit_ID(self, node):
        return self.symbol_table.get(node.value)
