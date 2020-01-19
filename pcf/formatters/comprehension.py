from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker


class Comprehension(Data, Formatter):
    @format_checker
    def format(self):
        yield from emit_comments(self.above_comment)
        yield " for "
        yield from self.target.format()
        yield " in "
        yield from self.iter.format()
        for i in self.ifs:
            yield " if "
            yield from i.format()
        yield from format_comment(self.line_comment)
