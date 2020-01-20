from mo_dots import Data
from pcf.utils import emit_comments, Formatter, format_checker, extra_comments


class Await(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):

        yield "await "
        yield from self.value.format()
