from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker


class Subscript(Data, Formatter):
    @format_checker
    def format(self):
        yield from emit_comments(self.above_comment)
        yield from self.value.format()
        yield "["
        yield from self.slice.format()
        yield "]"
        yield from format_comment(self.line_comment)
