from mo_dots import Data
from pcf.utils import emit_comments, emit_lines, format_comment, Formatter, format_checker


class If(Data, Formatter):
    @format_checker
    def format(self):
        yield from emit_comments(self.above_comment)
        yield "if "
        yield from format(self.test)
        yield ":"
        yield CR
        yield from format_comment(self.line_comment)
        yield from indent_body(self.body)
        if self.orelse:
            yield "else:"
            yield CR
            yield from indent_body(self.orelse)

