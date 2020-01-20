from mo_dots import Data
from pcf.utils import emit_comments, emit_lines, format_comment, Formatter, format_checker, extra_comments, SPACE


class ClassDef(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):

        yield from emit_lines(self.decorator_list)
        yield "class"
        yield SPACE
        yield self.node.name
        if self.node.bases:
            yield "("
            yield from self.node.bases
            yield ")"
        yield from format_comment(self.line_comment)
        yield from self.body.format()

