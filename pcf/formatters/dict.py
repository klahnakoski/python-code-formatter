import ast

from pcf.formatters import format
from pcf.utils import emit_comments, indent_lines, format_comment


class Dict(ast.Dict):

    def format(self):
        def items(separator=", "):
            sep = None
            for k, v in zip(self['keys'], self['values']):
                yield sep
                sep = separator
                yield from format(k)
                yield ": "
                yield from format(v)

        yield from emit_comments(self.above_comment)
        yield "{"
        yield from items(", ")
        yield "}"
        yield from format_comment(self.line_comment)

