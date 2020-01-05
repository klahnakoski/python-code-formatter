import ast

from pcf.formatters import format
from pcf.utils import emit_comments, optional_comment


class Return(ast.Return):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield "return "
        yield from format(self.value)
        yield from optional_comment(self.line_comment)

