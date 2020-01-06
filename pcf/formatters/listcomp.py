import ast

from pcf.formatters import format
from pcf.utils import emit_comments, format_comment, optional_comment


class ListComp(ast.ListComp):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield "["
        yield from optional_comment(self.line_comment)
        yield from format(self.elt)
        for g in self.generators:
            yield from format(g)
        yield "]"
