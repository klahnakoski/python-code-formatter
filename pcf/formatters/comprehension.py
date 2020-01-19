from mo_dots import Data
from pcf.utils import emit_comments, emit_lines, format_comment, Formatter, format_checker

class Comprehension(Data, Formatter):
    @format_checker
    def format(self):
        yield from emit_comments(self.above_comment)
        yield " for "
        yield from format(self.target)
        yield " in "
        yield from format(self.iter)
        for i in self.ifs:
            yield " if "
            yield from format(i)
        yield from format_comment(self.line_comment)
