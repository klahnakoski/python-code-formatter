from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker, extra_comments


class List(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):
        yield "["
        sep = None
        for v in self['elts']:
            yield sep
            sep = ", "
            yield from v.format()
        yield "]"
        yield from format_comment(self.line_comment)

