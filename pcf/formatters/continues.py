import ast

from pcf.utils import emit_comments, format_comment


class Continue(ast.Continue):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield "continue"
        yield from format_comment(self.line_comment)
