import sys

from src.parser import parser
from src.scanner import lexer
from src.TypeChecker import TypeChecker
from src.Interpreter import Interpreter


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "data/interpreter_examples/matrix.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    """Mparser = Mparser()
    parser = yacc.yacc(module=Mparser)"""
    text = file.read()
    ast = parser.parse(text, lexer=lexer)

    # Below code shows how to use visitor
    typeChecker = TypeChecker()   
    typeChecker.visit(ast)
    # typeChecker.print_errors()
    ast.accept(Interpreter())

    