#!/usr/bin/python
import AST
import scanner
import ply.yacc as yacc


tokens = scanner.tokens

precedence = (
    ("nonassoc", "IFX"),
    ("nonassoc", "ELSE"),
    ("nonassoc", '=', "ADDASSIGN", "SUBASSIGN", "MULASSIGN", "DIVASSIGN"),
    ("nonassoc", '<', '>', "LE", "GE", "NE", "EQ"),
    ("left", '+', '-'),
    ("left", '*', '/'),
    ("left", "DOTADD", "DOTSUB"),
    ("left", "DOTMUL", "DOTDIV"),
    ("left", "\'"),
    ("right", "UNARY")
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions_opt"""
    p[0] = p[1]

def p_instructions_opt_1(p):
    """instructions_opt : """
    p[0] = ''

def p_instructions_opt_2(p):
    """instructions_opt : instructions """
    p[0] = p[1]

def p_instructions_1(p):
    """instructions : instructions instruction """
    p[0] = AST.Node(p[1], p[2])

def p_instructions_2(p):
    """instructions : instruction """
    p[0] = p[1]

def p_instruction_b(p):
    """ instruction : '{' instructions '}' """
    p[0] = AST.Block(p[2])

def p_instruction(p):
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

def p_expr(p):
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


def p_expr1(p):
    """expr : '[' matrix_init ']' """
    p[0] = AST.Matrix(p[2])

def p_expr2(p):
    """expr : matrix_init_name '(' expr ')' """
    p[0] = AST.MatrixSpecialWord(p[1], p[3])

def p_expr3(p):
    """expr : INTNUM """
    p[0] = AST.IntNum(p[1])

def p_expr4(p):
    """expr : FLOATNUM """
    p[0] = AST.FloatNum(p[1])

def p_expr5(p):
    """expr : assignable """
    p[0] = p[1]

def p_expr6(p):
    """expr : '(' expr ')' """
    p[0] = p[2]

def p_expr7(p):
    """ expr : '-' expr %prec UNARY """
    p[0] = AST.UnaryMinus(p[2])

def p_expr8(p):
    """ expr : expr "\'" """
    p[0] = AST.UnaryTranspose(p[2])


def p_assignment_statement(p):
    """assignment_statement : assignable '=' expr
                            | assignable ADDASSIGN expr
                            | assignable SUBASSIGN expr
                            | assignable MULASSIGN expr
                            | assignable DIVASSIGN expr """
    p[0] = AST.BinaryExpr(p[2], p[1], p[3])


def p_assignable(p):
    """assignable : ID
                  | ID '[' expr ',' expr ']' """ # matrix_access

    if len(p) == 2:
        p[0] = AST.Variable(p[1])
    else:
        p[0] = AST.BinaryExpr(p[1] + "[,]", p[3], p[5])

def p_matrix_init(p):
    """matrix_init : '[' vector ']'
                   | matrix_init ',' '[' vector ']' """
    if len(p) == 4:
        p[0] = AST.Vector(p[2])
    else:
        p[0] = AST.Node(p[1], AST.Vector(p[4]))

def p_vector(p):
    """vector : expr
                    | vector ',' expr """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = AST.Node(p[1], p[3])

def p_matrix_init_name(p):
    """matrix_init_name : EYE
                        | ZEROS
                        | ONES """
    p[0] = p[1]



def p_if_statement(p):
    """if_statement : IF '(' expr ')' instruction %prec IFX
                    | IF '(' expr ')' instruction ELSE instruction """
    if len(p) == 8:
        p[0] = AST.IfElse(p[3], p[5], p[7])
    else:
        p[0] = AST.If(p[3], p[5])

def p_loop(p):
    """loop : for_loop
            | while_loop """
    p[0] = p[1]

def p_for_loop(p):
    """for_loop : FOR ID '=' range instruction """
    p[0] = AST.ForLoop(p[2], p[4], p[5])

def p_while_loop(p):
    """while_loop : WHILE '(' expr ')' instruction """
    p[0] = AST.WhileLoop(p[3], p[5])

def p_range(p):
    """range : expr ':' expr """
    p[0] = AST.BinaryExpr(p[2], p[1], p[3])

def p_print_statement(p):
    """print_statement : PRINT printables """
    p[0] = AST.PrintStatement(p[2])


def p_printables(p):
    """printables : printable 
                  | printables ',' printable """
    if len(p) == 2:
        p[0] = AST.Printable(p[1])
    else:
        p[0] = AST.Printable(p[1], p[3])

def p_printable1(p):
    """printable : expr """
    p[0] = p[1]

def p_printable2(p):
    """printable : STRING """
    p[0] = AST.String(p[1])

def p_return_statement(p):
    """return_statement : RETURN
                        | RETURN expr
                        | RETURN STRING """
    if len(p) == 2:
        p[0] = AST.ReturnStatement(p[1])
    else:
        p[0] = AST.ReturnStatement(p[1], p[2])
    

parser = yacc.yacc()
