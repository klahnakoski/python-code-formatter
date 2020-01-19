from mo_dots import Data
from pcf.utils import emit_comments, emit_lines, format_comment, Formatter, format_checker


class ImportFrom(Data, Formatter):
    @format_checker
    def format(self):
        yield from emit_comments(self.above_comment)
        yield "from "
        yield self.node.module
        yield " import "
        names = self.names
        if any(a.above_comment or a.line_comment for a in names):
            yield "("
            yield CR

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

        yield CR


