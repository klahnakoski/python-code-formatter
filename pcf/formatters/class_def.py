from mo_dots import Data
from pcf.utils import emit_comments, emit_lines, format_comment, Formatter, format_checker


class ClassDef(Data, Formatter):
    @format_checker
    def format(self):
        yield from emit_comments(self.above_comment)
        yield from emit_lines(self.decorator_list)
        yield "class "
        yield self.node.name
        if self.node.bases:
            yield "("
            yield from self.node.bases
            yield ")"
        yield from format_comment(self.line_comment)
        yield from self.body.format()

