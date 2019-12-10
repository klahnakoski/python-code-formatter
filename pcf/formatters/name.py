import ast

from pcf.formatters import format
from pcf.utils import emit_comments


class Name(ast.Name):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield self.node.id
        yield self.line_comment

