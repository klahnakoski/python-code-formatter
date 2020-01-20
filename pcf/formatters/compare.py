from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker, extra_comments


class Compare(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):
        yield from self.left.format()
        for o, c in zip(self.ops, self.comparators):
            yield from o.format()
            yield from c.format()
        yield from format_comment(self.line_comment)

