import ast

from pcf.utils import emit_comments, indent_body


class Try(ast.Try):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield "try:"
        yield self.line_comment
        yield "\n"
        yield from indent_body(self.body)
        for h in self.handlers:
            yield "\n"
            yield "except " + h.type.node.id
            # if h.type.node.ctx:
            #     yield from h.type.node.ctx
            yield ":"
            yield h.line_comment
            yield "\n"
            yield from indent_body(h.body)
        if self.orelse:
            yield "\n"
            yield "else:\n"
            yield from indent_body(self.orelse)
        if self.finalbody:
            yield "\n"
            yield "finally:\n"
            yield from indent_body(self.finalbody)

