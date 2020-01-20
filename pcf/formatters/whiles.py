from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker, extra_comments, indent_body, CR, SPACE


class While(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):

        yield "while"
        yield SPACE
        yield from self.test.format()
        yield ":"
        yield from format_comment(self.line_comment)
        yield CR
        yield from indent_body(self.body)
        if self.orelse:
            yield CR
            yield "else:"
            yield CR
            yield from indent_body(self.orelse)
