from mo_dots import Data
from pcf.utils import emit_comments, emit_lines, format_comment, Formatter, format_checker


class Return(Data, Formatter):
    @format_checker
    def format(self):
        yield from emit_comments(self.above_comment)
        yield "return "
        yield from format(self.value)
        yield from format_comment(self.line_comment)
        yield CR

