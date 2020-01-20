from mo_dots import Data
from pcf.utils import emit_comments, format_comment, Formatter, format_checker, extra_comments, CR, SPACE


class Import(Data, Formatter):
    @format_checker
    @extra_comments
    def format(self):

        aliases = self.node.names
        for a in aliases:
            yield "import"
            yield SPACE
            yield a.name
            if a.asname:
                yield SPACE
                yield "as"
                yield SPACE
                yield a.asname
            yield from format_comment(self.line_comment)
        yield CR

