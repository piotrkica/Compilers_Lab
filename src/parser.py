from src import scanner
import ply.yacc as yacc
from src import AST

tokens = scanner.tokens

precedence = (
    ("nonassoc", 'IF_END'),
    ('nonassoc', 'ELSE'),
    ("right", "=", ":"),
    ('left', 'LESSER_THAN', 'GREATER_THAN', 'LESSER_EQUAL', 'GREATER_EQUAL', 'NOT_EQUAL', 'EQUAL'),
    ("left", 'DOTADD', 'DOTSUB', '+', '-'),
    ("left", 'DOTMUL', 'DOTDIV', '*', '/'),
    ('left', "'"),
    # ('right', 'UMINUS')
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions """
    p[0] = p[1]


def p_instructions_2(p):
    """instructions : instructions instruction """
    p[0] = AST.InstructionDoubler(p[1], p[2])


def p_instructions_1(p):
    """instructions : instruction """
    p[0] = p[1]


def p_instruction(p):
    """instruction : assign_instr
                   | if_instr
                   | while_instr
                   | for_instr
                   | break_instr
                   | continue_instr
                   | return_instr
                   | print_instr
                   | expression """
    p[0] = p[1]


def p_instruction_in(p):
    """instruction : '{' instructions '}' """
    p[0] = p[2]


def p_assign_instr(p):
    """assign_instr : ID '=' expression ';'
                    | ID PLUSASSIGN expression ';'
                    | ID SUBASSIGN expression ';'
                    | ID MULASSIGN expression ';'
                    | ID DIVASSIGN expression ';'
                    | ID '=' array ';' """
    p[0] = AST.AssignInstr(p[2], p[1], p[3])


def p_assign_instr_ref(p):  # rozszerzone
    """assign_instr : ID '[' indexes ']' '=' expression ';'
                    | ID '[' indexes ']' PLUSASSIGN expression ';'
                    | ID '[' indexes ']' SUBASSIGN expression ';'
                    | ID '[' indexes ']' MULASSIGN expression ';'
                    | ID '[' indexes ']' DIVASSIGN expression ';' """
    p[0] = AST.AssignInstrRef(p[5], p[1], p[3], p[6])


def p_assign_instr_other(p):  # TODO trzeba albo naprawic uminusa albo napisac case dla tego
    """assign_instr : ID '=' '-' expression ';' """


def p_arrays_1(p):
    """array : '[' subarrays ']'
             | '[' indexes ']' """
    p[0] = AST.Vector(p[2])


def p_subarrays_2(p):
    """subarrays : subarrays ',' subarray"""
    p[0] = AST.SubarrayDoubler(p[1], p[3])


def p_subarrays_1(p):
    """subarrays : subarray """
    p[0] = p[1]


def p_subarray(p):
    """subarray : array """
    p[0] = p[1]


def p_indexes_2(p):
    """ indexes : indexes ',' index """
    p[0] = AST.IndexDoubler(p[1], p[3])


def p_indexes_1(p):
    """ indexes : index"""
    p[0] = p[1]


def p_index_int(p):
    """ index : INTNUM """
    p[0] = AST.IntNum(p[1])

def p_index_id(p):
    """ index : ID """
    p[0] = AST.ID(p[1])


def p_if_instr(p):
    """if_instr : IF '(' expression ')' instruction %prec IF_END """
    p[0] = AST.If(p[3], p[5])


def p_if_else_instr(p):
    """if_instr : IF '(' expression ')' instruction ELSE instruction """
    p[0] = AST.IfElse(p[3], p[5], p[7])


def p_while_instr(p):
    """while_instr : WHILE '(' expression ')' instruction """
    p[0] = AST.While(p[3], p[5])


def p_for_instr(p):
    """for_instr : FOR range instruction """
    p[0] = AST.For(p[2], p[3])


def p_range(p):
    """range : ID '=' expression ':' expression """
    p[0] = AST.Range(p[1], p[3], p[5])


def p_break_instr(p):
    """break_instr : BREAK ';' """
    p[0] = AST.Break(p[1])


def p_continue_instr(p):
    """continue_instr : CONTINUE ';' """
    p[0] = AST.Continue(p[1])


def p_return_instr_1(p):
    """return_instr : RETURN ';' """
    p[0] = AST.Return(p[1])


def p_return_instr_2(p):
    """return_instr : RETURN expression ';' """
    p[0] = AST.ReturnExpression(p[1], p[2])


def p_print_instr(p):
    """print_instr : PRINT printable ';' """
    p[0] = AST.Print(p[1], p[2])


def p_printable_2(p):
    """printable : printable ',' expression """
    p[0] = AST.PrintDoubler(p[1], p[3])


def p_printable_1(p):
    """printable : expression """
    p[0] = p[1]


def p_comparison(p):
    """expression : expression LESSER_THAN expression
                  | expression GREATER_THAN expression
                  | expression LESSER_EQUAL expression
                  | expression GREATER_EQUAL expression
                  | expression NOT_EQUAL expression
                  | expression EQUAL expression """
    p[0] = AST.BinExpr(p[2], p[1], p[3])


# def p_unary(p):
#     """expression : '-' expression %prec UMINUS"""


def p_basic_operations(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression """
    p[0] = AST.BinExpr(p[2], p[1], p[3])


def p_matrix_operations(p):
    """expression : expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression """
    p[0] = AST.MatrixBinExpr(p[2], p[1], p[3])


def p_matrix_transformation(p):
    """expression : expression "'" """
    p[0] = AST.Transpose(p[1])


def p_matrix_declarations(p):
    """expression : EYE '(' expression ')'
                  | ONES '(' expression ')'
                  | ZEROS '(' expression ')' """
    p[0] = AST.MatrixDeclarations(p[1], p[3])


def p_parentheses(p):
    """expression : '(' expression ')'"""
    p[0] = p[2]


def p_expression_int(p):
    """expression : INTNUM """
    p[0] = AST.IntNum(p[1])


def p_expression_float(p):
    """expression : FLOATNUM"""
    p[0] = AST.FloatNum(p[1])


def p_expression_string(p):
    """expression : STRING """
    p[0] = AST.String(p[1])


def p_expression_id(p):
    """expression : ID """
    p[0] = AST.ID(p[1])


parser = yacc.yacc()
