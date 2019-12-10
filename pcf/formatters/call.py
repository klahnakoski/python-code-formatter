import ast

from pcf.formatters import format
from pcf.utils import emit_comments


class Call(ast.Call):

    def format(self):
        yield from emit_comments(self.above_comment)
        if self.is_decorator:
            yield "@"
        yield from format(self.func)
        yield "("
        comma = None
        for a in self.args:
            yield comma
            comma = ", "
            yield from format(a)
        for a in self.keywords:
            yield comma
            comma = ", "
            yield from format(a)
        yield ")"
        yield self.line_comment

