from mo_dots import Data
from pcf.utils import emit_comments, emit_lines, format_comment, Formatter, format_checker, indent_body


class While(Data, Formatter):
    @format_checker
    def format(self):
        yield from emit_comments(self.above_comment)
        yield "while "
        yield from format(self.test)
        yield from format_comment(self.line_comment)
        yield from indent_body(self.body)

        if self.orelse:
            yield CR
            yield "else "
            yield from indent_body(self.orelse)
