import ast

from pcf.utils import emit_comments, indent_body, emit_lines


class AsyncFunctionDef(ast.AsyncFunctionDef):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield from emit_lines(self.decorator_list)
        yield "async def " + self.node.name + "("
        yield self.line_comment
        for a in self.node.args.args:
            yield a.arg
        yield "):\n"
        yield from indent_body(self.body)
