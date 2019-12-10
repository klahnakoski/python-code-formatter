import ast

from pcf.formatters import format
from pcf.utils import emit_comments, indent_body


class If(ast.If):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield "if "
        yield from format(self.test)
        yield ":\n"
        yield from indent_body(self.body)
        if self.orelse:
            yield "else:\n"
            yield from indent_body(self.body)

