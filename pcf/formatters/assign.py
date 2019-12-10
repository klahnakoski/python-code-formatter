import ast

from pcf.formatters import format
from pcf.utils import emit_comments, join


class Assign(ast.Assign):

    def format(self):
        yield from emit_comments((self.above_comment))
        yield from join(self.targets, ", ")
        yield " = "
        yield from format(self.value)
        yield self.line_comment
        yield "\n"

