from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker


class Continue(Data, Formatter):
    @format_checker
    def format(self):
        yield from emit_comments(self.above_comment)
        yield "continue"
        yield from format_comment(self.line_comment)
