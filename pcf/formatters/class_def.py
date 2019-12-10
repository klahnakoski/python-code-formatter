import ast

from pcf.utils import emit_comments, indent_body, emit_lines


class ClassDef(ast.ClassDef):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield from emit_lines(self.decorator_list)
        yield "class "
        yield self.node.name
        if self.node.bases:
            yield "("
            yield from self.node.bases
            yield ")"
        yield ":"
        yield self.line_comment
        yield "\n"
        yield from indent_body(self.body)

