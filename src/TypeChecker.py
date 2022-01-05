from collections import defaultdict

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

for oper in ['==', "!=", '+']:
    type_map[oper]["str"]["str"] = "str"


class NodeVisitor(object):
    symbol_table = SymbolTable(None, 'init')
    loop_depth = 0
    errors = []  # TODO error w której linii

    def print_errors(self):
        for error in self.errors:
            print(error)

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        print("visiting method: " + method)
        # print(node)
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
        print()
        self.visit(node.right)

    def visit_AssignInstr(self, node):
        type_right = self.visit(node.right)
        if node.op == "=":
            if type_right != 'any':
                self.symbol_table.put(node.left.value, type_right)
            else:
                self.errors.append("Wrong type in assignment")
                print("Wrong type in assignment")
            print(self.symbol_table.symbols.items())
        else:
            if node.left.value not in self.symbol_table.symbols:
                self.errors.append("Missing symbol in line")
            else:
                type_left = self.symbol_table.get(node.left.value)
                new_type = type_map[node.op][type_left][type_right]
                if new_type != 'any':
                    self.symbol_table[node.left.value] = new_type
                else:
                    self.errors.append("Wrong type in assignment")
                    print("Wrong type in assignment")

    def visit_AssignInstrRef(self, node):
        # copy assignInstr?
        pass

    def visit_AssignUnary(self, node):
        type_expr = self.visit(node.expr)
        if type_expr not in ["int", "float"]:
            self.errors.append("Wrong type in unary assignment")
        self.symbol_table.put(node.id.value, type_expr)

    def visit_Vector(self, node):  # todo weryfikacja wymiarów
        self.visit(node.vector)
        return "Vector"

    def visit_SubarrayDoubler(self, node):
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)

    def visit_IndexDoubler(self, node):
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)
        if type_left != "int" or type_right != "int":
            self.errors.append("Wrong index type in line ...")
            print("Wrong index type in line ...")
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
            self.errors.append("Wrong type in range")

    def visit_Break(self, node):
        if self.loop_depth <= 0:
            self.errors.append("Break usage outside loop")

    def visit_Continue(self, node):
        if self.loop_depth <= 0:
            self.errors.append("Continue usage outside loop")

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
        self.visit(node.left)
        self.visit(node.right)

    def visit_Transpose(self, node):
        self.visit(node.left)

    def visit_MatrixDeclarations(self, node):
        type_expr = self.visit(node.expr)
        if type_expr != "int":
            self.errors.append("Wrong type in matrix declaration")
        return "vector"

    def visit_IntNum(self, node):
        return "int"

    def visit_FloatNum(self, node):
        return "float"

    def visit_String(self, node):
        return "str"

    def visit_ID(self, node):
        return self.symbol_table.get(node.value)
