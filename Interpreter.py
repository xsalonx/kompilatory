import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *
import sys

sys.setrecursionlimit(10000)


def mul(x, y):
    # TODO
    return x * y


def dot_add(x, y):
    if not (len(x) == len(y) and len(x[0]) == len(y[0])):
        raise Exception("Wrong matrix sizes")
    else:
        return [[x[row][col] + y[row][col] for col in range(len(x[0]))] for row in range(len(x))]


def dot_sub(x, y):
    if not (len(x) == len(y) and len(x[0]) == len(y[0])):
        raise Exception("Wrong matrix sizes")
    else:
        return [[x[row][col] - y[row][col] for col in range(len(x[0]))] for row in range(len(x))]


def dot_mul(x, y):
    if not (len(x) == len(y) and len(x[0]) == len(y[0])):
        raise Exception("Wrong matrix sizes")
    else:
        return [[x[row][col] * y[row][col] for col in range(len(x[0]))] for row in range(len(x))]


def dot_div(x, y):
    if not (len(x) == len(y) and len(x[0]) == len(y[0])):
        raise Exception("Wrong matrix sizes")
    else:
        return [[x[row][col] / y[row][col] for col in range(len(x[0]))] for row in range(len(x))]


def unary_minus(x):
    if isinstance(x, list):
        return [[(-1) * x[row][col] for col in range(len(x[0]))] for row in range(len(x))]
    return (-1) * x


class Interpreter(object):

    def __init__(self):
        self.scopes = MemoryStack()
        self.op_dict = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': mul,
            '/': lambda x, y: x / y,
            '.+': dot_add,
            '.-': dot_sub,
            '.*': dot_mul,
            './': dot_div,
            '+=': lambda var, x, y: self.scopes.set(var, x + y),
            '-=': lambda var, x, y: self.scopes.set(var, x - y),
            '*=': lambda var, x, y: self.scopes.set(var, x * y),
            '/=': lambda var, x, y: self.scopes.set(var, x / y),
            '<': lambda x, y: x < y,
            '>': lambda x, y: x > y,
            '<=': lambda x, y: x <= y,
            '>=': lambda x, y: x >= y,
            '!=': lambda x, y: x != y,
            '==': lambda x, y: x == y,
            'unary_minus': unary_minus,
            'eye': lambda size: [[1 if i == j else 0 for j in range(size)] for i in range(size)],
            'zeros': lambda size: [[0 for j in range(size)] for i in range(size)],
            'ones': lambda size: [[1 for j in range(size)] for i in range(size)]
        }

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Node)
    def visit(self, node):
        self.visit(node.left)
        self.visit(node.right)

    @when(AST.Scope)
    def visit(self, node):
        pass

    @when(AST.IntNum)
    def visit(self, node):
        return node.value

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.String)
    def visit(self, node):
        return node.string   # TODO czy to jest ok ? (czemu node.string[1:-1])

    @when(AST.Variable)
    def visit(self, node):
        return self.scopes.get(node.name)

    @when(AST.BinaryExpr)
    def visit(self, node):
        pass

    @when(AST.Range)
    def visit(self, node):
        return range(node._from, node.to)

    @when(AST.Ref)
    def visit(self, node):
        pass

    @when(AST.UnaryMinus)
    def visit(self, node):
        r = self.visit(node.expr)
        return self.op_dict['unary_minus'](r)

    @when(AST.UnaryTranspose)
    def visit(self, node):
        prev = self.visit(node.expr)
        new = []
        rows = len(prev)
        cols = len(prev[0])
        for col in range(cols):
            new_row = []
            for row in range(rows):
                new_row.append(prev[row][col])
            new.append(new_row)
        return new

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
        raise BreakException()

    @when(AST.ContinueInstruction)
    def visit(self, node):
        raise ContinueException()

    @when(AST.ReturnStatement)
    def visit(self, node):
        value = self.visit(node.value)
        raise ReturnValueException(value)

    @when(AST.Printable)
    def visit(self, node):
        return self.visit(node.printable)

    @when(AST.PrintStatement)
    def visit(self, node):
        text = ""
        for printable in node.content:
            r = self.visit(printable)
            text += str(r) + " "
        print(text)

    @when(AST.MatrixSpecialWord)
    def visit(self, node):
        size = self.visit(node.value)
        return self.op_dict[node.word](size)

    @when(AST.Vector)
    def visit(self, node):
        result = []
        for val in node.inside:
            r = self.visit(val)
            result.append(r)
        return result

    @when(AST.Matrix)
    def visit(self, node):
        result = []
        for row in node.inside:
            r = self.visit(row)
            result.append(r)
        return result

    @when(AST.Error)
    def visit(self, node):
        raise Exception(f'Compiling failed. Error in line {node.lineno}')

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
