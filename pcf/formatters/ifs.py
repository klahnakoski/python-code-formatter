import ast

from pcf.formatters import format
from pcf.utils import emit_comments, format_comment


class If(ast.If):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield "if "
        yield from format(self.test)
        yield from format_comment(self.line_comment)
        yield from format(self.body)
        if self.orelse:
            yield "else"
            yield from format(self.body)

