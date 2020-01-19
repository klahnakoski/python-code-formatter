from mo_dots import Data
from mo_logs import Log
from mo_logs.strings import quote
from pcf.utils import emit_comments, emit_lines, format_comment, Formatter, format_checker


class Constant(Data, Formatter):

    @format_checker
    def format(self):
        yield from emit_comments(self.previous.above_comment)
        yield from format_comment(self.previous.line_comment)
        yield from emit_comments(self.above_comment)

        value = self.node.value
        if isinstance(value, str):
            if self.is_multiline_string:
                yield '"""' + value + '"""'
            else:
                yield quote(value)
        elif isinstance(value, (float, int)):
            yield str(value)
        elif value is None:
            yield "None"
        elif isinstance(value, type(...)):
            yield "..."
        elif isinstance(value, bytes):
            yield repr(value)
        else:
            Log.error(
                "do not know how to handle {{type}}", type=value.__class__.__name__
            )

        format_comment(self.line_comment)
