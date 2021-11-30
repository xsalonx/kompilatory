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
    """instructions_opt : instructions """
    p[0] = p[1]

def p_instructions_opt_2(p):
    """instructions_opt : """
    p[0] = ''

def p_instructions_1(p):
    """instructions : instructions instruction """
    p[0] = AST.Node(p[1], p[2])

def p_instructions_2(p):
    """instructions : instruction """
    p[0] = p[1]

def p_instructions_3(p):
    """instructions : '{' instructions '}' """
    p[0] = AST.Block(p[2])

def p_instructions_4(p):
    """instructions : '{' instructions '}' instructions"""
    p[0] = AST.Node(AST.Block(p[2]), p[4])

def p_instruction(p):
    """instruction : expr ';'
                   | assignment_statement ';'
                   | if_statement
                   | loop
                   | BREAK ';'
                   | CONTINUE ';'
                   | print_statement ';'
                   | return_statement ';' """

def p_expr(p):
    """expr : assignable
            | FLOATNUM
            | INTNUM
            | matrix_init_name '(' expr ')'
            | '[' matrix_init ']'
            | '-' expr %prec UNARY
            | expr "\'"
            | expr '+' expr
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
            | expr EQ expr
            | '(' expr ')' """

def p_assignment_statement(p):
    """assignment_statement : assignable '=' expr
                            | assignable ADDASSIGN expr
                            | assignable SUBASSIGN expr
                            | assignable MULASSIGN expr
                            | assignable DIVASSIGN expr """

def p_assignable(p):
    """assignable : ID
                  | matrix_access """

def p_matrix_access(p):
    """matrix_access : ID '[' expr ',' expr ']' """

def p_matrix_init(p):
    """matrix_init : '[' vector ']'
                   | matrix_init ',' '[' vector ']' """

def p_vector(p):
    """vector : expr
                    | vector ',' expr """

def p_matrix_init_name(p):
    """matrix_init_name : EYE
                        | ZEROS
                        | ONES """

def p_if_statement(p):
    """if_statement : IF '(' expr ')' instructions %prec IFX
                    | IF '(' expr ')' instructions ELSE instructions """

def p_loop(p):
    """loop : for_loop
            | while_loop """

def p_for_loop(p):
    """for_loop : FOR ID '=' range instructions """

def p_while_loop(p):
    """while_loop : WHILE '(' expr ')' instructions """

def p_range(p):
    """range : expr ':' expr """

def p_print_statement(p):
    """print_statement : PRINT printables """

def p_printables(p):
    """printables : printable 
                  | printables ',' printable """

def p_printable(p):
    """printable : STRING
                 | expr """

def p_return_statement(p):
    """return_statement : RETURN
                        | RETURN expr
                        | RETURN STRING """
    

parser = yacc.yacc()
