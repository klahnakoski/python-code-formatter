from mo_dots import Data
from pcf.utils import emit_comments, emit_lines, format_comment, Formatter, format_checker


class Keyword(Data, Formatter):
    @format_checker
    def format(self):
        yield self.node.arg
        yield "="
        yield from format(self.value)

