from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker, extra_comments


class Subscript(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):

        yield from self.value.format()
        yield "["
        yield from self.slice.format()
        yield "]"
        yield from format_comment(self.line_comment)
