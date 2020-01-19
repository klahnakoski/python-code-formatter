from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker


class Call(Data, Formatter):
    @format_checker
    def format(self):
        yield from emit_comments(self.above_comment)
        if self.is_decorator:
            yield "@"
        yield from self.func.format()
        yield "("
        comma = None
        for a in self.args:
            yield comma
            comma = ", "
            yield from a.format()
        for a in self.keywords:
            yield comma
            comma = ", "
            yield from a.format()
        yield ")"
        yield from format_comment(self.line_comment)

