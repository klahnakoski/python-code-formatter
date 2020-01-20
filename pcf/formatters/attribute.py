from mo_dots import Data
from pcf.utils import emit_comments, Formatter, format_checker, extra_comments


class Attribute(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):

        yield from self.value.format()
        yield "."
        yield self.node.attr

