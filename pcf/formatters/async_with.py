from mo_dots import Data
from pcf.utils import Formatter, format_checker
from pcf.utils import emit_comments, format_comment


class AsyncWith(Data, Formatter):
    @format_checker
    def format(node):
        yield from emit_comments(node.above_comment)
        yield "async with "
        comma = False
        for w in node["items"]:
            if comma:
                yield ", "
            comma = True
            yield from w.context_expr.format()
            if w.optional_vars:
                yield " as "
                yield w.optional_vars.id
        yield from format_comment(node.line_comment)
        yield from node.body.format()
