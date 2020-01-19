from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker


class ListComp(Data, Formatter):
    @format_checker
    def format(self):
        yield from emit_comments(self.above_comment)
        yield "["
        yield from format_comment(self.line_comment)
        yield from self.elt.format()
        for g in self.generators:
            yield from g.format()
        yield "]"
