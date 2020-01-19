from mo_dots import Data
from pcf.utils import emit_comments, emit_lines, format_comment, Formatter, format_checker


class Dict(Data, Formatter):
    @format_checker
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

