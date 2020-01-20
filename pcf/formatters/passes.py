from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker, extra_comments


class Pass(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):
        yield "pass"
        yield from format_comment(self.line_comment)
