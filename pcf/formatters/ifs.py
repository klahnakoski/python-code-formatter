from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker, extra_comments, CR, indent_body, SPACE


class If(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):

        yield "if"
        yield SPACE
        yield from self.test.format()
        yield ":"
        yield CR
        yield from format_comment(self.line_comment)
        yield from indent_body(self.body)
        if self.orelse:
            yield "else:"
            yield CR
            yield from indent_body(self.orelse)

