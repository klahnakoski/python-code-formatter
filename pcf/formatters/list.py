from mo_dots import Data, Null
from pcf.utils import format_comment, Formatter, format_checker, extra_comments, CR, indent_lines


class List(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):
        yield "["
        yield from csv(self['elts'])
        yield "]"
        yield from format_comment(self.line_comment)


def csv(values):
    if len(values) == 0:
        pass
    elif len(values) == 1 and not values[0].is_multiline():
        yield from values[0].format()
    else:
        def elements():
            sep = None
            for v in values:
                yield sep
                sep = ","
                yield CR
                yield from v.format()
        yield CR
        yield from indent_lines(elements())
        yield CR
