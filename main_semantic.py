import sys
import ply.yacc as yacc
from src.parser import parser
from src.scanner import lexer
from src.TypeChecker import TypeChecker

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "data/semantic_examples/init.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    ast = parser.parse(text, lexer=lexer)

    # Below code shows how to use visitor
    typeChecker = TypeChecker()
    typeChecker.visit(ast)
