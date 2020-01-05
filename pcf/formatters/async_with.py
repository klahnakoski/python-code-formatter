import ast

from pcf.formatters import format
from pcf.utils import emit_comments, format_comment


class AsyncWith(ast.AsyncWith):

    def format(node):
        yield from emit_comments(node.above_comment)
        yield "async with "
        comma = False
        for w in node['items']:
            if comma:
                yield ", "
            comma = True
            yield from format(w.context_expr)
            if w.optional_vars:
                yield " as "
                yield w.optional_vars.id
        yield from format_comment(node.line_comment)
        yield from format(node.body)

