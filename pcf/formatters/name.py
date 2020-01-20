from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker, extra_comments


class Name(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):
        yield self.node.id
        yield from format_comment(self.line_comment)

