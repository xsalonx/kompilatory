import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *
import sys

sys.setrecursionlimit(10000)


class Interpreter(object):

    def __init__(self):
        pass

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Node)
    def visit(self, node):
        pass

    @when(AST.Scope)
    def visit(self, node):
        pass

    @when(AST.IntNum)
    def visit(self, node):
        pass

    @when(AST.FloatNum)
    def visit(self, node):
        pass

    @when(AST.String)
    def visit(self, node):
        pass

    @when(AST.Variable)
    def visit(self, node):
        pass

    @when(AST.BinaryExpr)
    def visit(self, node):
        pass

    @when(AST.Range)
    def visit(self, node):
        pass

    @when(AST.Ref)
    def visit(self, node):
        pass

    @when(AST.UnaryMinus)
    def visit(self, node):
        pass

    @when(AST.UnaryTranspose)
    def visit(self, node):
        pass

    @when(AST.IfStatement)
    def visit(self, node):
        pass

    @when(AST.ForLoop)
    def visit(self, node):
        pass

    @when(AST.WhileLoop)
    def visit(self, node):
        pass

    @when(AST.BreakInstruction)
    def visit(self, node):
        pass

    @when(AST.ContinueInstruction)
    def visit(self, node):
        pass

    @when(AST.ReturnStatement)
    def visit(self, node):
        pass

    @when(AST.Printable)
    def visit(self, node):
        pass

    @when(AST.PrintStatement)
    def visit(self, node):
        pass

    @when(AST.MatrixSpecialWord)
    def visit(self, node):
        pass

    @when(AST.Vector)
    def visit(self, node):
        pass

    @when(AST.Matrix)
    def visit(self, node):
        pass

    @when(AST.Error)
    def visit(self, node):
        pass

    """

    @when(AST.BinOp)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval

    @when(AST.Assignment)
    def visit(self, node):
    #
    #

    # simplistic while loop interpretation
    @when(AST.WhileInstr)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.body.accept(self)
        return r
        
    """
