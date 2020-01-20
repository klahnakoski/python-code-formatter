from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker, extra_comments, indent_body, CR


class While(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):

        yield "while "
        yield from self.test.format()
        yield from format_comment(self.line_comment)
        yield from indent_body(self.body)

        if self.orelse:
            yield CR
            yield "else "
            yield from indent_body(self.orelse)
