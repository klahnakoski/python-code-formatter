import ast

from pcf.formatters import format
from pcf.utils import emit_comments, emit_lines, format_comment


class ClassDef(ast.ClassDef):

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
        yield from format(self.body)

