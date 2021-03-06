#!/usr/bin/python
import AST
import SymbolTable
from collections import defaultdict

symtable = SymbolTable.SymbolTable(None, "symtable")
ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))

ttype['+']["int"]["int"] = "int"
ttype['-']["int"]["int"] = "int"
ttype['*']["int"]["int"] = "int"
ttype['/']["int"]["int"] = "int"
ttype[".+"]["int"]["int"] = "int"
ttype[".-"]["int"]["int"] = "int"
ttype[".*"]["int"]["int"] = "int"
ttype["./"]["int"]["int"] = "int"
ttype['<']["int"]["int"] = "logic"
ttype['>']["int"]["int"] = "logic"
ttype["<="]["int"]["int"] = "logic"
ttype[">="]["int"]["int"] = "logic"
ttype["=="]["int"]["int"] = "logic"
ttype["!="]["int"]["int"] = "logic"

ttype['+']["int"]["float"] = "float"
ttype['-']["int"]["float"] = "float"
ttype['*']["int"]["float"] = "float"
ttype['/']["int"]["float"] = "float"
ttype[".+"]["int"]["float"] = "float"
ttype[".-"]["int"]["float"] = "float"
ttype[".*"]["int"]["float"] = "float"
ttype["./"]["int"]["float"] = "float"
ttype['<']["int"]["float"] = "logic"
ttype['>']["int"]["float"] = "logic"
ttype["<="]["int"]["float"] = "logic"
ttype[">="]["int"]["float"] = "logic"
ttype["=="]["int"]["float"] = "logic"
ttype["!="]["int"]["float"] = "logic"

ttype['+']["float"]["int"] = "float"
ttype['-']["float"]["int"] = "float"
ttype['*']["float"]["int"] = "float"
ttype['/']["float"]["int"] = "float"
ttype[".+"]["float"]["int"] = "float"
ttype[".-"]["float"]["int"] = "float"
ttype[".*"]["float"]["int"] = "float"
ttype["./"]["float"]["int"] = "float"
ttype['<']["float"]["int"] = "logic"
ttype['>']["float"]["int"] = "logic"
ttype["<="]["float"]["int"] = "logic"
ttype[">="]["float"]["int"] = "logic"
ttype["=="]["float"]["int"] = "logic"
ttype["!="]["float"]["int"] = "logic"

ttype['+']["float"]["float"] = "float"
ttype['-']["float"]["float"] = "float"
ttype['*']["float"]["float"] = "float"
ttype['/']["float"]["float"] = "float"
ttype[".+"]["float"]["float"] = "float"
ttype[".-"]["float"]["float"] = "float"
ttype[".*"]["float"]["float"] = "float"
ttype["./"]["float"]["float"] = "float"
ttype['<']["float"]["float"] = "logic"
ttype['>']["float"]["float"] = "logic"
ttype["<="]["float"]["float"] = "logic"
ttype[">="]["float"]["float"] = "logic"
ttype["=="]["float"]["float"] = "logic"
ttype["!="]["float"]["float"] = "logic"

castable_operations = ['/', '+', '-', '*', '>', '<', ">=", "<=", "==", "!="]
castable_matrix_operations = [".+", ".-", ".*", "./"]
castable_types = ["int", "float"]


class Error:
    errors = {
        "no_var": "Undeclared variable",
        "no_loop_scope_break": "Break instruction outside the loop",
        "no_loop_scope_continue": "Continue instruction outside the loop",
        "not_logic": "Not a logical statement",
        "inv_range": "Incorrect range expressions types",
        "inv_transpose": "Trying to transpose a non-matrix",
        "inv_mat_arg": "Invalid matrix size argument",
        "inv_mat_arg_types": "Invalid matrix arguments types (not ints)",
        "inv_mat_arg_values": "Invalid matrix arguments values",
        "error": "Error found by parser",
        "diff_ty": "Different types"
    }

    def __init__(self, code, lineno):
        self.code = code
        self.lineno = lineno

    def __str__(self):
        return f'{self.errors[self.code]} in line {self.lineno}'


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)

        return visitor(node)

    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):

    def visit_Node(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Scope(self, node):
        symtable.pushScope("scope")
        self.visit(node.instructions)
        symtable.popScope()

    def visit_BinaryExpr(self, node):
        op = node.op
        type2 = self.visit(node.right)

        if op == '=':
            if hasattr(node.left, 'op'):
                type1 = self.visit(node.left)
                if type1 != type2:
                    print(Error('diff_ty', node.lineno))
                    return None
                return None
            else:
                if type2:
                    symtable.put(node.left.name, type2)
                return None



        type1 = self.visit(node.left)
        if op in castable_operations and type1 in castable_types and type2 in castable_types:
            return ttype[op][type1][type2]

        if isinstance(type1, tuple) and isinstance(type2, tuple):
            rows1, cols1, vals1 = type1[0], type1[1], type1[2]
            rows2, cols2, vals2 = type2[0], type2[1], type2[2]
            if not (rows1 == rows2 and cols1 == cols2):
                print(Error('wr_mat_sizes_op', node.lineno))
                return None
            if not (op, vals1, vals2) in ttype:
                print(Error('diff_ty', node.lineno))
                return None
            return (rows1, cols1, ttype[op][vals1][vals2])

        if op in castable_matrix_operations:  # matrix op on non-matrix type
            print(Error('mat_op_on_non_mat', node.lineno))
            return None

        if type1 != type2:
            print(Error('diff_ty', node.lineno))
            return None

        print(op)
        return ttype[op][type1][type2]

    def visit_Variable(self, node):
        var = symtable.get(node.name)
        if var is None:
            print(Error("no_var", node.lineno))
            return None
        return var

    def visit_IntNum(self, node):
        return "int"

    def visit_FloatNum(self, node):
        return "float"

    def visit_String(self, node):
        return "str"

    def visit_Range(self, node):
        t1 = self.visit(node._from)
        t2 = self.visit(node.to)

        return "int" if t1 == t2 == "int" else None

    def visit_Ref(self, node):
        type1 = self.visit(node.x)
        type2 = self.visit(node.y)
        tmp = symtable
        var = node.var
        varAST = symtable.get(var.name)
        var_type = varAST.type

        if not isinstance(var_type, tuple):
            print(Error("no_var", node.lineno))
            return None
        rows, cols, mat_type = var_type[0], var_type[1], var_type[2]
        if type1 == type2 == "int":
            if hasattr(node.x, "value") and (
                    node.x.value <= 0 or node.x.value > rows or node.y.value <= 0 or node.y.value > cols):
                print(Error("inv_mat_arg_values", node.lineno))
                return None
            return mat_type
        else:
            print(Error("inv_mat_arg_types", node.lineno))
            return None

    def visit_UnaryMinus(self, node):
        self.visit(node.expr)

    def visit_UnaryTranspose(self, node):
        type1 = self.visit(node.expr)
        if not isinstance(type1, tuple):
            print(Error("inv_transpose", node.lineno))
            return None
        return type1[1], type1[0], type1[2]

    def visit_IfStatement(self, node):
        type1 = self.visit(node.condition)
        if type1 != "logic":
            print(Error("not_logic", node.lineno))
        symtable.pushScope("if")
        self.visit(node.ifBlock)
        symtable.popScope()
        if node.elseBlock is not None:
            symtable.pushScope("else")
            self.visit(node.elseBlock)
            symtable.popScope()

    def visit_ForLoop(self, node):
        type1 = self.visit(node._range)
        if type1 != "int":
            print(Error("inv_range", node.lineno))
        symtable.put(node.var.name, type1)
        symtable.pushScope("loop")
        self.visit(node.block)
        symtable.popScope()

    def visit_WhileLoop(self, node):
        type1 = self.visit(node.condition)
        if type1 != "logic":
            print(Error("not_logic", node.lineno))
        symtable.pushScope("loop")
        self.visit(node.block)
        symtable.popScope()

    def visit_BreakInstruction(self, node):
        loop_scope = symtable.getScope("loop")
        if loop_scope is None:
            print(Error("no_loop_scope_break", node.lineno))

    def visit_ContinueInstruction(self, node):
        loop_scope = symtable.getScope("loop")
        if loop_scope is None:
            print(Error("no_loop_scope_continue", node.lineno))

    def visit_ReturnStatement(self, node):
        if node.value:
            self.visit(node.value)

    def visit_Printable(self, node):
        self.visit(node.printable)

    def visit_PrintStatement(self, node):
        n = node
        while isinstance(n, AST.Node):
            self.visit(n.right)
            n = n.left
        # TODO


    def visit_MatrixSpecialWord(self, node):
        type1 = self.visit(node.value)
        if type1 != "int":
            print(Error("inv_mat_arg", node.lineno))
        size = node.value.value
        return size, size, "int"

    def visit_Vector(self, node):
        n = node.inside
        ts = self.visit(n.right)
        l = 0
        while isinstance(n, AST.Node):
            if ts != self.visit(n.right):
                print(Error("diff_ty", node.lineno))
            n = n.left
            l += 1
        # TODO
        return l, ts

    def visit_Matrix(self, node):
        n = node
        s, t = self.visit(n.right)
        l = 0
        while isinstance(n, AST.Node):
            if self.visit(n.right) != (s, t):
                print(Error("diff_ty", node.lineno))
            n = n.left
            l += 1
        return l, s, t

    def visit_Error(self, node):
        print(Error("error", node.lineno))
