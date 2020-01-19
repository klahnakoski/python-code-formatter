from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker


class Name(Data, Formatter):
    @format_checker
    def format(self):
        yield from emit_comments(self.previous.above_comment)
        yield from format_comment(self.previous.line_comment)
        yield from emit_comments(self.above_comment)
        yield self.node.id
        yield from format_comment(self.line_comment)

