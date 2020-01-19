from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker


class Tuple(Data, Formatter):
    @format_checker
    def format(self):
        yield from emit_comments(self.above_comment)
        yield "("
        yield from format_comment(self.line_comment)
        sep = None
        for v in self['elts']:
            yield sep
            sep = ", "
            yield from v.format()
        yield ")"

