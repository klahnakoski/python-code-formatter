import ast

from pcf.formatters import format
from pcf.utils import emit_comments, join, optional_comment


class Compare(ast.Compare):

    def format(self):
        yield from emit_comments((self.above_comment))
        yield from format(self.left)
        for o, c in zip(self.ops, self.comparators):
            yield from format(o)
            yield from format(c)
        yield from optional_comment(self.line_comment)

