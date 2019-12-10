import ast

from pcf.formatters import format
from pcf.utils import emit_comments, indent_body, emit_lines
from mo_future import zip_longest


class FunctionDef(ast.FunctionDef):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield from emit_lines(self.decorator_list)
        yield "def " + self.node.name + "("
        yield self.line_comment
        for a, d in zip_longest(self.args.args, self.args.defaults):
            yield a.arg
            if d:
                yield "="
                yield from format(d)
        yield "):"
        yield self.line_comment
        yield "\n"
        yield from indent_body(self.body)
