import ast

from pcf.formatters import format
from pcf.utils import emit_comments, indent_lines, format_comment


class List(ast.List):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield "["
        yield from format_comment(self.line_comment)
        sep = None
        for v in self['elts']:
            yield sep
            sep = ", "
            yield from format(v)
        yield "]"

