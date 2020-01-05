import ast

from pcf.utils import emit_comments, format_comment


class Name(ast.Name):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield self.node.id
        yield from format_comment(self.line_comment)

