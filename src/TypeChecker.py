from src import AST
from src.SymbolTable import SymbolTable


class NodeVisitor(object):
    symbol_table = SymbolTable(None, 'init')
    errors = []

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        print("visiting method: " + method)
        print(node)
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


class TypeChecker(NodeVisitor):  # TODO kiedy coś zwracać a kiedy nie
    def visit_InstructionDoubler(self, node):
        self.visit(node.left)
        print()
        self.visit(node.right)

    def visit_AssignInstr(self, node):
        type_right = self.visit(node.right)
        if node.op == "=":
            self.symbol_table.put(node.left.value, type_right)
            print(self.symbol_table.symbols.items())
        else:
            if node.left not in self.symbol_table.symbols:
                print("missing symbol")
                self.errors.append("Missing symbol in ...")
            else:
                type_left = self.symbol_table.get(node.left.value)
                # TODO EWALUACJA TYPU

    def visit_AssignInstrRef(self, node):
        pass

    def visit_AssignUnary(self, node):
        type_expr = self.visit(node.expr)
        # TODO SPRAWDŹ TYP
        self.symbol_table.put(node.id.value, type_expr)

    def visit_Vector(self, node):
        # o panie tu jest roboty tyle ze
        pass

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
        self.symbol_table = self.symbol_table.pushScope("While")
        self.visit(node.expr)
        self.visit(node.instr)
        self.symbol_table = self.symbol_table.popScope()

    def visit_For(self, node):
        self.symbol_table = self.symbol_table.pushScope("For")
        self.visit(node.range)
        self.visit(node.instr)
        self.symbol_table = self.symbol_table.popScope()

    def visit_Range(self, node):
        type_expr1 = self.visit(node.expr1)
        type_expr2 = self.visit(node.expr2)
        # TODO sprawdz typy expr1 i expr2

    def visit_Break(self, node):
        # TODO check for break usage outside loops
        pass

    def visit_Continue(self, node):
        # TODO check for continue usage outside loops
        pass

    def visit_Return(self, node):
        # TODO check for return usage outside function????
        pass

    def visit_ReturnExpression(self, node):
        # TODO check for return usage outside function????
        self.visit(node.expr)

    def visit_Print(self, node):
        self.visit(node.expr)

    def visit_PrintDoubler(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_BinExpr(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_MatrixBinExpr(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Transpose(self, node):
        self.visit(node.left)

    def visit_MatrixDeclarations(self, node):
        self.visit(node.expr)

    def visit_IntNum(self, node):
        return "int"

    def visit_FloatNum(self, node):
        return "float"

    def visit_String(self, node):
        return "str"

    def visit_ID(self, node):
        return self.symbol_table.get(node.value)
