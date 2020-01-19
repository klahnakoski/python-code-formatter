from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker


class Expr(Data, Formatter):
    @format_checker
    def format(self):
        yield from emit_comments(self.above_comment)
        yield from self.value.format()
        yield from format_comment(self.line_comment)
        yield self.eol
