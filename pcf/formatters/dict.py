from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker


class Dict(Data, Formatter):
    @format_checker
    def format(self):
        def items(separator=", "):
            sep = None
            for k, v in zip(self['keys'], self['values']):
                yield sep
                sep = separator
                yield from k.format()
                yield ": "
                yield from v.format()

        yield from emit_comments(self.above_comment)
        yield "{"
        yield from items(", ")
        yield "}"
        yield from format_comment(self.line_comment)

