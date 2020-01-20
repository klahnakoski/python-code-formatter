from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker, extra_comments


class ListComp(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):

        yield "["
        yield from format_comment(self.line_comment)
        yield from self.elt.format()
        for g in self.generators:
            yield from g.format()
        yield "]"
