from mo_dots import Data
from pcf.utils import emit_comments, Formatter, format_checker, extra_comments, SPACE


class Await(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):

        yield "await"
        yield SPACE
        yield from self.value.format()
