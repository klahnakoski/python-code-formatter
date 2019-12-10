import ast

from pcf.formatters import format
from pcf.utils import emit_comments


class Import(ast.Import):

    def format(self):
        yield from emit_comments(self.above_comment)
        aliases = self.node.names
        for a in aliases:
            yield "import " + a.name
            if a.asname:
                yield " as " + a.asname
            yield self.line_comment
        yield "\n"

