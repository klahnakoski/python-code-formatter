from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker, extra_comments, CR, SPACE


class Try(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):

        yield "try"
        yield from format_comment(self.line_comment)
        yield from self.body.format()
        for h in self.handlers:
            yield CR
            yield "except"
            yield SPACE
            yield h.type.node.id
            yield from format_comment(h.line_comment)
            yield from h.body.format()
        if self.orelse:
            yield CR
            yield "else"
            yield from format_comment(self.orelse.line_comment)
            yield from self.orelse.format()
        if self.finalbody:
            yield CR
            yield "finally"
            yield from format_comment(self.finalbody.line_comment)
            yield from self.finalbody.format()
