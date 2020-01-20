from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker, extra_comments

def nothing():
    yield None


class Ins(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):
        yield " in "


class BoolOp(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):
        op = nothing()
        for v in self['values']:
            yield from op
            op = self.op.format()
            yield from v.format()
        yield from format_comment(self.line_comment)


class And(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):
        yield " and "


class IsNot(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):
        yield " is not "


class Is(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):
        yield " is "


class BinOp(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):

        yield from self.left.format()
        yield from self.op.format()
        yield from self.right.format()
        yield from format_comment(self.line_comment)


class Add(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):
        yield " + "


class UnaryOp(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):

        yield from self.op.format()
        yield from self.operand.format()
        yield from format_comment(self.line_comment)


class USub(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):
        yield " -"


