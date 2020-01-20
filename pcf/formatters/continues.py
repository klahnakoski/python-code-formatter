from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker, extra_comments


class Continue(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):

        yield "continue"
        yield from format_comment(self.line_comment)
