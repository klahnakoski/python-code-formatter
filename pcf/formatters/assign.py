from mo_dots import Data
from pcf.utils import emit_comments, join, format_comment, CR, format_checker, extra_comments, Formatter, SPACE


class Assign(Data, Formatter):

    @format_checker
    @extra_comments
    def format(self):
        yield from join(self.targets, ", ")
        yield SPACE
        yield "="
        yield SPACE
        yield from self.value.format()
        yield from format_comment(self.line_comment)
        yield CR

