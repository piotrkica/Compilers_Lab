from src import scanner
import ply.yacc as yacc

tokens = scanner.tokens

# TODO: add uminus operator and similar (check literals in scanner)
# TODO: rethink p_if_instr
# TODO: infinite else ifs
# TODO: split expressions to functions (at the end)

precedence = (
    ("nonassoc", 'IF_END'),
    ('nonassoc', 'ELSE'),
    ('left', 'LESSER_THAN', 'GREATER_THAN', 'LESSER_EQUAL', 'GREATER_EQUAL', 'NOT_EQUAL', 'EQUAL'),
    ("right", "=", ":"),
    ('left', ','),
    ("left", '+', '-'),
    ("left", '*', '/'),
    ('left', 'DOTADD', 'DOTSUB'),
    ('left', 'DOTMUL', 'DOTDIV'),
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions"""


def p_instructions(p):
    """instructions : instructions instruction
                    | instructions '{' instructions '}'
                    | instruction """


def p_instruction(p):
    """instruction : assign_instr
                   | if_instr
                   | while_instr
                   | for_instr
                   | break_instr
                   | continue_instr
                   | return_instr
                   | print_instr
                   | expression
                    """

def p_assign_instr(p):
    """assign_instr : ID '=' expression ';'
                    | ID '=' '-' expression ';'
                    | ID PLUSASSIGN expression ';'
                    | ID SUBASSIGN expression ';'
                    | ID MULASSIGN expression ';'
                    | ID DIVASSIGN expression ';'
                    | ID '[' indexes ']' '=' expression ';'
                    | ID '=' arrays ';'
                    """

def p_arrays(p):
    """arrays :  '[' arrays ']'
              | arrays ',' arrays
              | '[' indexes ']'
    """

def p_indexes(p):
    """ indexes : indexes ',' index
                | index
    """

def p_index(p):
    """ index : INTNUM
              | ID
    """

def p_if_instr(p):
    """if_instr : IF '(' expression ')' '{' instructions '}' %prec IF_END
                | IF '(' expression ')' instruction %prec IF_END
                | IF '(' expression ')' instruction ELSE instruction
                | IF '(' expression ')' instruction ELSE '{' instructions '}'
                | IF '(' expression ')' '{' instructions '}' ELSE instruction
                | IF '(' expression ')' '{' instructions '}' ELSE '{' instructions '}'"""


def p_while_instr(p):
    """while_instr : WHILE '(' instruction ')' instruction
                   | WHILE '(' instruction ')' '{' instructions '}' """

def p_for_instr(p):
    """for_instr : FOR range instruction
                 | FOR range '{' instruction '}' """

def p_range(p):
    """range : ID '=' expression ':' expression"""

def p_break_instr(p):
    """break_instr : BREAK ';' """

def p_continue_instr(p):
    """continue_instr : CONTINUE ';' """

def p_return_instr(p):
    """return_instr : RETURN expression ';' """

def p_print_instr(p):
    """print_instr : PRINT printable ';' """

def p_printable(p):
    """printable : printable ',' expression
                 | expression"""

def p_expression(p):
    """expression : expression LESSER_THAN expression
                  | expression GREATER_THAN expression
                  | expression LESSER_EQUAL expression
                  | expression GREATER_EQUAL expression
                  | expression NOT_EQUAL expression
                  | expression EQUAL expression
                  | expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression
                  | '(' expression ')'
                  | '(' '-' expression ')'
                  | EYE '(' expression ')'
                  | ONES '(' expression ')'
                  | ZEROS '(' expression ')'
                  | expression "\'"
                  | FLOATNUM
                  | INTNUM
                  | STRING
                  | ID
                  """


parser = yacc.yacc()
