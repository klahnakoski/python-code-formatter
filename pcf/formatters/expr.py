import ast

from pcf.formatters import format
from pcf.utils import emit_comments, format_comment


class Expr(ast.Expr):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield from format(self.value)
        yield from format_comment(self.line_comment)

