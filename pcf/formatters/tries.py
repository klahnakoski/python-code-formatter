import ast

from pcf.formatters import format
from pcf.utils import emit_comments, optional_comment, format_comment


class Try(ast.Try):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield "try"
        yield from format_comment(self.line_comment)
        yield from format(self.body)
        for h in self.handlers:
            yield "\n"
            yield "except " + h.type.node.id
            yield from format_comment(h.line_comment)
            yield from format(h.body)
        if self.orelse:
            yield "\n"
            yield "else"
            yield from format_comment(self.orelse.line_comment)
            yield from format(self.orelse)
        if self.finalbody:
            yield "\n"
            yield "finally"
            yield from format_comment(self.finalbody.line_comment)
            yield from format(self.finalbody)
