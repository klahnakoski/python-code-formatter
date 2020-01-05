import ast

from pcf.utils import emit_comments, format_comment


class Import(ast.Import):

    def format(self):
        yield from emit_comments(self.above_comment)
        aliases = self.node.names
        for a in aliases:
            yield "import " + a.name
            if a.asname:
                yield " as " + a.asname
            yield from format_comment(self.line_comment)
        yield "\n"

