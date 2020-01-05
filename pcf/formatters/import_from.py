import ast

from pcf.utils import emit_comments, indent_lines, format_comment


class ImportFrom(ast.ImportFrom):

    def format(self):
        yield from emit_comments(self.above_comment)
        yield "from " + self.node.module + " import "
        names = self.names
        if any(a.above_comment or a.line_comment for a in names):
            yield "(\n"

            def import_lines():
                for a in names:
                    yield a.above_comment
                    yield a.node.name
                    if a.node.asname:
                        yield " as " + a.node.asname
                    yield from format_comment(a.line_comment)

            yield from indent_lines(import_lines())
            yield ")"
        else:
            # PACK THE IMPORT
            yield self.above_comment
            yield ", ".join(
                a.node.name + (" as " + a.node.asname if a.node.asname else "")
                for a in names
            )
            yield from format_comment(self.line_comment)


