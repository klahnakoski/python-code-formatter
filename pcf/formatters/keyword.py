from mo_dots import Data
from pcf.utils import Formatter, format_checker, extra_comments


class Keyword(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):
        yield self.node.arg
        yield "="
        yield from self.value.format()

