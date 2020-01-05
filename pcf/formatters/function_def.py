import ast

from mo_future import zip_longest
from pcf.formatters import format
from pcf.utils import emit_comments, emit_lines, format_comment


class FunctionDef(ast.FunctionDef):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield from emit_lines(self.decorator_list)
        yield "def " + self.node.name + "("
        yield from format_comment(self.line_comment)
        for a, d in zip_longest(self.args.args, self.args.defaults):
            yield a.arg
            if d:
                yield "="
                yield from format(d)
        yield ")"
        yield from format_comment(self.line_comment)
        yield from format(self.body)
