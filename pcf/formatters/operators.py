import ast

from pcf.utils import format, emit_comments, optional_comment, format_comment


def nothing():
    yield None


class Ins(ast.In):

    def format(self):
        yield "in"


class BoolOp(ast.In):

    def format(self):
        yield from emit_comments(self.above_comment)
        op = nothing()
        for v in self['values']:
            yield from op
            op = format(self.op)
            yield from format(v)
        yield from format_comment(self.line_comment)


class And(ast.And):

    def format(self):
        yield "and"


class IsNot(ast.IsNot):
    def format(self):
        yield "is not"

class Is(ast.Is):
    def format(self):
        yield "is"


class BinOp(ast.BinOp):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield from format(self.left)
        yield from format(self.op)
        yield from format(self.right)
        yield from format_comment(self.line_comment)


class Add(ast.Add):

    def format(self):
        yield "+"


class UnaryOp(ast.BinOp):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield from format(self.op)
        yield from format(self.operand)
        yield from format_comment(self.line_comment)


class USub(ast.USub):

    def format(self):
        yield "-"


