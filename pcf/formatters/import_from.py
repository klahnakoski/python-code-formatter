from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker, extra_comments, CR, indent_lines, SPACE


class ImportFrom(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):

        yield "from"
        yield SPACE
        yield self.node.module
        yield SPACE
        yield "import"
        yield SPACE
        names = self.names
        if any(n.is_multiline(limit=120-len(self.node.module)-13) for n in names) or 120 < sum(len(n.name) for n in names)+len(self.node.module)+13:
            yield "("
            yield CR

            def import_lines():
                for a in names:
                    yield a.node.name
                    if a.node.asname:
                        yield SPACE
                        yield "as"
                        yield SPACE
                        yield a.node.asname
                    yield from format_comment(a.line_comment)

            yield from indent_lines(import_lines())
            yield CR
            yield ")"
            yield from format_comment(self.line_comment)

        else:
            # PACK THE IMPORT
            yield self.before_comment
            yield ", ".join(
                a.node.name + (" as " + a.node.asname if a.node.asname else "")
                for a in names
            )
            yield from format_comment(self.line_comment)

        yield CR


