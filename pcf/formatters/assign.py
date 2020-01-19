from mo_dots import Data
from pcf.utils import emit_comments, join, format_comment, CR, format_checker, Formatter


class Assign(Data, Formatter):

    @format_checker
    def format(self):
        yield from emit_comments((self.previous.above_comment))
        yield from format_comment(self.previous.line_comment)
        yield from emit_comments((self.above_comment))
        yield from join(self.targets, ", ")
        yield " = "
        yield from self.value.format()
        yield from format_comment(self.line_comment)
        yield CR

