import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *
import sys

sys.setrecursionlimit(10000)



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

def create_fil_ndarray(sizes, fil):
    result = []
    if len(sizes) == 1:
        return [fil] * sizes[0]
    for i in range(sizes[0]):
        result.append(create_fil_ndarray(sizes[1:], fil))
    return result

def create_square_eye_ndarray(sizes, fil):
    v = sizes[0]
    if not all([v == s for s in sizes]):
        raise Exception("Wrong sizes of nd eye matrix")
    M = create_fil_ndarray(sizes, 0)
    for i in range(v):
        submatrix = M
        for depth in range(len(sizes) - 1):
            submatrix = submatrix[i]
        submatrix[i] = fil
    return M




class Interpreter(object):

    def __init__(self):
        self.scopes = MemoryStack(Memory('global'))
        self.op_dict = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '.+': dot_add,
            '.-': dot_sub,
            '.*': dot_mul,
            './': dot_div,
            '<': lambda x, y: x < y,
            '>': lambda x, y: x > y,
            '<=': lambda x, y: x <= y,
            '>=': lambda x, y: x >= y,
            '!=': lambda x, y: x != y,
            '==': lambda x, y: x == y,
            'unary_minus': unary_minus,
            'eye': lambda sizes: create_square_eye_ndarray(sizes, 1),
            'zeros': lambda sizes: create_fil_ndarray(sizes, 0),
            'ones': lambda sizes: create_fil_ndarray(sizes, 1)
        }
        self.assignment_op_dict = {
            '+=': lambda var, y: self.scopes.set(var, self.scopes.get(var) + y),
            '-=': lambda var, y: self.scopes.set(var, self.scopes.get(var) - y),
            '*=': lambda var, y: self.scopes.set(var, self.scopes.get(var) * y),
            '/=': lambda var, y: self.scopes.set(var, self.scopes.get(var) / y),
            '=': lambda var, x: self.scopes.set(var, x),
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
        self.visit(node.instructions)

    @when(AST.IntNum)
    def visit(self, node):
        return node.value

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.String)
    def visit(self, node):
        return node.string[1:-1]

    @when(AST.Variable)
    def visit(self, node):
        return self.scopes.get(node.name)

    @when(AST.BinaryExpr)
    def visit(self, node):
        op = node.op
        if op in self.assignment_op_dict:
            if isinstance(node.left, AST.Ref):
                M = self.scopes.get(node.left.var.name)
                row = node.left.x.value
                col = node.left.y.value
                v = self.visit(node.right)
                if op[0] == '=':
                    M[row][col] = v
                else:
                    M[row][col] = self.op_dict[op[0]](M[row][col], v)
            else:
                self.assignment_op_dict[op](node.left.name, self.visit(node.right))
        else:
            vl = self.visit(node.left)
            vr = self.visit(node.right)
            return self.op_dict[op](vl, vr)

    @when(AST.Range)
    def visit(self, node):
        fr = self.visit(node.from_)
        to = self.visit(node.to)
        return range(fr, to)

    @when(AST.Ref)
    def visit(self, node):
        M = self.scopes.get(node.var.name)
        row = node.x.value
        col = node.y.value
        return M[row][col]

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
        if self.visit(node.condition):
            self.visit(node.ifBlock)
        elif node.elseBlock is not None:
            self.visit(node.elseBlock)

    @when(AST.ForLoop)
    def visit(self, node):
        range_ = self.visit(node.range_)
        varname = node.var.name
        for _i in range_:
            try:
                self.scopes.set(varname, _i)
                self.visit(node.block)
            except ReturnValueException as e:
                return e.value
            except BreakException as e:
                break
            except ContinueException as e:
                continue

    @when(AST.WhileLoop)
    def visit(self, node):
        cond_node = node.condition
        while self.visit(cond_node):
            try:
                self.visit(node.block)
            except ReturnValueException as e:
                return e.value
            except BreakException as e:
                break
            except ContinueException as e:
                continue

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
        p = node.content
        while isinstance(p, AST.Node):
            text += str(self.visit(p.right)) + " "
            p = p.left
        text += str(self.visit(p))
        print(text)

    @when(AST.MatrixSpecialWord)
    def visit(self, node):
        sizes = self.visit(AST.Vector(node.value))
        if len(sizes) == 1:
            sizes *= 2
        return self.op_dict[node.word](sizes)

    @when(AST.Vector)
    def visit(self, node):
        result = []
        n = node.inside
        while isinstance(n, AST.Node):
            result = [self.visit(n.right)] + result
            n = n.left
        result = [self.visit(n)] + result
        return result

    @when(AST.Matrix)
    def visit(self, node):
        result = []
        n = node.inside
        while isinstance(n, AST.Node):
            result = [self.visit(n.right)] + result
            n = n.left
        result = [self.visit(n)] + result
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
