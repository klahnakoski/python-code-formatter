import ast

from pcf.formatters import format
from pcf.utils import emit_comments, format_comment, optional_comment


class Comprehension(ast.comprehension):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield "for"
        yield from format(self.target)
        yield "in"
        yield from format(self.iter)
        for i in self.ifs:
            yield from format(i)
        yield from format_comment(self.line_comment)
