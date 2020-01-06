import ast

from pcf.utils import emit_comments, format_comment


class Pass(ast.Pass):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield "pass"
        yield from format_comment(self.line_comment)
