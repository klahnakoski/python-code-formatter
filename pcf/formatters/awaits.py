import ast

from pcf.formatters import format
from pcf.utils import emit_comments


class Await(ast.Await):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield "await "
        yield from format(self.value)
