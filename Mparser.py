#!/usr/bin/python

import scanner
import ply.yacc as yacc
import AST

is_error = False

tokens = scanner.tokens

scopes = []


def push_scope(s):
    print("push")
    pass


def pop_scope(s):
    print("pop")
    pass


precedence = (
    ("nonassoc", "IFX"),
    ("nonassoc", "ELSE"),
    ("nonassoc", '=', "ADDASSIGN", "SUBASSIGN", "MULASSIGN", "DIVASSIGN"),
    ("nonassoc", '<', '>', "LE", "GE", "NE", "EQ"),
    ("left", '+', '-'),
    ("left", "DOTADD", "DOTSUB"),

    ("left", '*', '/'),
    ("left", "DOTMUL", "DOTDIV"),

    ("left", "\'"),
    ("right", "UNARY")
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
        global is_error
        is_error = True
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions_opt"""
    p[0] = p[1]


def p_instructions_opt_1(p):
    """instructions_opt : """
    p[0] = None


def p_instructions_opt_2(p):
    """instructions_opt : instructions """
    p[0] = p[1]


def p_instructions_1(p):
    """instructions : instructions instruction """
    p[0] = AST.Node(p[1], p[2])


def p_instructions_2(p):
    """instructions : instruction """
    p[0] = p[1]


def p_scopestart(p):
    """ scopestart : """
    p[0] = AST.Scope("start")
    push_scope(scopes)


def p_scopeend(p):
    """ scopeend : """
    p[0] = AST.Scope("end")
    pop_scope(scopes)


def p_instruction_1(p):
    """ instruction : '{' scopestart instructions scopeend '}' """
    p[0] = p[3]


def p_instruction_2(p):
    """instruction : expr ';'
                   | assignment_statement ';'
                   | if_statement
                   | loop
                   | BREAK ';'
                   | CONTINUE ';'
                   | print_statement ';'
                   | return_statement ';' """
    if p[1] == "break":
        p[0] = AST.BreakInstruction()
    elif p[1] == "continue":
        p[0] = AST.ContinueInstruction()
    else:
        p[0] = p[1]


def p_expr_1(p):
    """expr : expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr
            | expr DOTADD expr
            | expr DOTSUB expr
            | expr DOTMUL expr
            | expr DOTDIV expr
            | expr '<' expr
            | expr '>' expr
            | expr LE expr
            | expr GE expr
            | expr NE expr
            | expr EQ expr """
    p[0] = AST.BinaryExpr(p[2], p[1], p[3])


def p_expr_2(p):
    """expr : '[' matrix_init ']' """
    p[0] = AST.Vector(p[2])


def p_expr_3(p):
    """expr : matrix_init_name '(' expr ')' """
    p[0] = AST.MatrixSpecialWord(p[1], p[3])


def p_expr_4(p):
    """expr : INTNUM """
    p[0] = AST.IntNum(p[1])


def p_expr_5(p):
    """expr : FLOATNUM """
    p[0] = AST.FloatNum(p[1])


def p_expr_6(p):
    """expr : assignable """
    p[0] = p[1]


def p_expr_7(p):
    """expr : '(' expr ')' """
    p[0] = p[2]


def p_expr_8(p):
    """ expr : '-' expr %prec UNARY """
    p[0] = AST.UnaryMinus(p[2])


def p_expr_9(p):
    """ expr : expr "\'" """
    p[0] = AST.UnaryTranspose(p[1])


def p_assignment_statement(p):
    """assignment_statement : assignable '=' expr
                            | assignable ADDASSIGN expr
                            | assignable SUBASSIGN expr
                            | assignable MULASSIGN expr
                            | assignable DIVASSIGN expr """
    p[0] = AST.BinaryExpr(p[2], p[1], p[3])


def p_assignable(p):
    """assignable : ID
                  | ID '[' expr ',' expr ']' """
    p[0] = AST.Variable(p[1]) if len(p) == 2 else AST.Ref(AST.Variable(p[1]), p[3], p[5])


def p_matrix_init(p):
    """matrix_init : '[' vector ']'
                   | matrix_init ',' '[' vector ']' """
    p[0] = AST.Vector(p[2]) if len(p) == 4 else AST.Node(p[1], AST.Vector(p[4]))


def p_vector(p):
    """vector : expr
              | vector ',' expr """
    p[0] = p[1] if len(p) == 2 else AST.Node(p[1], p[3])


def p_matrix_init_name(p):
    """matrix_init_name : EYE
                        | ZEROS
                        | ONES """
    p[0] = p[1]


def p_if_statement(p):
    """if_statement : IF '(' expr ')' instruction %prec IFX
                    | IF '(' expr ')' instruction ELSE instruction """
    p[0] = AST.IfStatement(p[3], p[5], p[7]) if len(p) == 8 else AST.IfStatement(p[3], p[5])


def p_loop(p):
    """loop : for_loop
            | while_loop """
    p[0] = p[1]


def p_for_loop(p):
    """for_loop : FOR ID '=' range instruction """
    p[0] = AST.ForLoop(AST.Variable(p[2]), p[4], p[5])


def p_while_loop(p):
    """while_loop : WHILE '(' expr ')' instruction """
    p[0] = AST.WhileLoop(p[3], p[5])


def p_range(p):
    """range : expr ':' expr """
    p[0] = AST.Range(p[1], p[3])


def p_print_statement(p):
    """print_statement : PRINT printables """
    p[0] = AST.PrintStatement(p[2])


def p_printables(p):
    """printables : printable
                  | printables ',' printable """
    p[0] = AST.Printable(p[1]) if len(p) == 2 else AST.Node(p[1], AST.Printable(p[3]))


def p_printable_1(p):
    """printable : expr """
    p[0] = p[1]


def p_printable_2(p):
    """printable : STRING """
    p[0] = AST.String(p[1])


def p_return_statement_1(p):
    """return_statement : RETURN """
    p[0] = AST.ReturnStatement()


def p_return_statement_2(p):
    """return_statement : RETURN expr """
    p[0] = AST.ReturnStatement(p[2])


def p_return_statement_3(p):
    """return_statement : RETURN STRING """
    p[0] = AST.ReturnStatement(AST.String(p[2]))


parser = yacc.yacc()
