import ast

from pcf.formatters import format
from pcf.utils import emit_comments


class Attribute(ast.Attribute):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield from format(self.value)
        yield "."
        yield from self.node.attr

