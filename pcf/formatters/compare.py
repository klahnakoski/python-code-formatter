from mo_dots import Data
from pcf.utils import emit_comments, emit_lines, format_comment, Formatter, format_checker


class Compare(Data, Formatter):
    @format_checker
    def format(self):
        yield from emit_comments((self.previous.above_comment))
        yield from format_comment(self.previous.line_comment)
        yield from emit_comments((self.above_comment))
        yield from format(self.left)
        for o, c in zip(self.ops, self.comparators):
            yield from format(o)
            yield from format(c)
        yield from format_comment(self.line_comment)

