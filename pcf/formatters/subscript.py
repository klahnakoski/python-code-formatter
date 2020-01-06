import ast

from pcf.formatters import format
from pcf.utils import emit_comments, format_comment, optional_comment


class Subscript(ast.Subscript):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield from format(self.value)
        yield "["
        yield from format(self.slice)
        yield "]"
        yield from format_comment(self.line_comment)
