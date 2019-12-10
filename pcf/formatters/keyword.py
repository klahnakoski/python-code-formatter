import ast

from pcf.formatters import format
from pcf.utils import emit_comments


class Keyword(ast.keyword):

    def format(self):
        yield self.node.arg
        yield "="
        yield from format(self.value)

