from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker, extra_comments, SPACE


class Comprehension(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):

        yield SPACE
        yield "for"
        yield SPACE
        yield from self.target.format()
        yield SPACE
        yield "in"
        yield SPACE
        yield from self.iter.format()
        for i in self.ifs:
            yield SPACE
            yield "if"
            yield SPACE
            yield from i.format()
        yield from format_comment(self.line_comment)
