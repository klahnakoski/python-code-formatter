from mo_dots import Data
from pcf.utils import emit_comments, emit_lines, format_comment, Formatter, format_checker


class Try(Data, Formatter):
    @format_checker
    def format(self):
        yield from emit_comments(self.above_comment)
        yield "try"
        yield from format_comment(self.line_comment)
        yield from format(self.body)
        for h in self.handlers:
            yield CR
            yield "except " + h.type.node.id
            yield from format_comment(h.line_comment)
            yield from format(h.body)
        if self.orelse:
            yield CR
            yield "else"
            yield from format_comment(self.orelse.line_comment)
            yield from format(self.orelse)
        if self.finalbody:
            yield CR
            yield "finally"
            yield from format_comment(self.finalbody.line_comment)
            yield from format(self.finalbody)
