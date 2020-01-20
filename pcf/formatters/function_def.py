from mo_dots import Data
from mo_future import zip_longest
from pcf.utils import emit_comments, emit_lines, format_comment, Formatter, format_checker, extra_comments, CR, indent_body


class FunctionDef(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):

        yield from emit_lines(self.decorator_list)
        yield "def "
        yield self.node.name
        yield "("
        yield from format_comment(self.line_comment)
        for a, d in zip_longest(self.args.args, self.args.defaults):
            yield a.arg
            if d:
                yield "="
                yield from d.format()
        yield "):"
        yield from format_comment(self.line_comment)
        yield CR
        yield from indent_body(self.body)
