from mo_dots import Data
from pcf.utils import emit_comments, Formatter, format_checker


class Attribute(Data, Formatter):
    @format_checker
    def format(self):
        yield from emit_comments(self.above_comment)
        yield from self.value.format()
        yield "."
        yield self.node.attr

