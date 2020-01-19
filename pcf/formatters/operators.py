from mo_dots import Data
from pcf.utils import emit_comments, emit_lines, format_comment, Formatter, format_checker

def nothing():
    yield None


class Ins(Data, Formatter):
    @format_checker
    def format(self):
        yield " in "


class BoolOp(Data, Formatter):
    @format_checker
    def format(self):
        yield from emit_comments(self.previous.above_comment)
        yield from format_comment(self.previousline_comment)
        yield from emit_comments(self.above_comment)
        op = nothing()
        for v in self['values']:
            yield from op
            op = format(self.op)
            yield from format(v)
        yield from format_comment(self.line_comment)


class And(Data, Formatter):
    @format_checker
    def format(self):
        yield " and "


class IsNot(Data, Formatter):
    @format_checker
    def format(self):
        yield " is not "


class Is(Data, Formatter):
    @format_checker
    def format(self):
        yield " is "


class BinOp(Data, Formatter):
    @format_checker
    def format(self):
        yield from emit_comments(self.above_comment)
        yield from format(self.left)
        yield from format(self.op)
        yield from format(self.right)
        yield from format_comment(self.line_comment)


class Add(Data, Formatter):
    @format_checker
    def format(self):
        yield " + "


class UnaryOp(Data, Formatter):
    @format_checker
    def format(self):
        yield from emit_comments(self.above_comment)
        yield from format(self.op)
        yield from format(self.operand)
        yield from format_comment(self.line_comment)


class USub(Data, Formatter):
    @format_checker
    def format(self):
        yield " -"


