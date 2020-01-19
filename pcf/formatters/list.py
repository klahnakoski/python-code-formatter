from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker


class List(Data, Formatter):
    @format_checker
    def format(self):
        yield from emit_comments(self.previous.above_comment)
        yield "["
        yield from format_comment(self.previous.line_comment)
        yield from emit_comments(self.above_comment)
        yield from format_comment(self.line_comment)
        sep = None
        for v in self['elts']:
            yield sep
            sep = ", "
            yield from v.format()
        yield "]"

