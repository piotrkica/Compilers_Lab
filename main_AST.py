import sys
import ply.yacc as yacc
from src.scanner import lexer
from src.parser import parser
from src.TreePrinter import TreePrinter

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "data/ast_examples/example3.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    # Mparser = parser()
    # parser_ = yacc.yacc(module=parser)
    text = file.read()
    ast = parser.parse(text, lexer=lexer)
    ast.printTree()
