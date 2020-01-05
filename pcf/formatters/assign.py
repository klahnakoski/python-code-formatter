import ast

from pcf.formatters import format
from pcf.utils import emit_comments, join, format_comment, optional_comment


class Assign(ast.Assign):

    def format(self):
        yield from emit_comments((self.above_comment))
        yield from join(self.targets, ", ")
        yield " = "
        yield from format(self.value)
        yield from optional_comment(self.line_comment)

