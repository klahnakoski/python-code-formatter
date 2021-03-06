from mo_dots import Data
from pcf.utils import emit_comments, emit_lines, format_comment, Formatter, format_checker, extra_comments


class AsyncFunctionDef(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):

        yield from emit_lines(self.decorator_list)
        yield "async def " + self.node.name + "("
        yield from format_comment(self.line_comment)
        for a in self.node.args.args:
            yield a.arg
        yield ")"
        yield from self.body.format()
