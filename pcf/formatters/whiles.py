import ast

from pcf.formatters import format
from pcf.utils import emit_comments, optional_comment, format_comment


class While(ast.While):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield "while"
        yield from format(self.test)
        yield from format_comment(self.line_comment)
        yield from format(self.body)

        if self.orelse:
            yield "\n"
            yield "else"
            yield from format(self.orelse)
