from mo_dots import Data
from pcf.utils import emit_comments, emit_lines, format_comment, Formatter, format_checker

class Module(Data, Formatter):
    @format_checker
    def format(self):
        # FIND IMPORTS
        s = e = 0
        for i, c in enumerate(self.body):
            if isinstance(c.node, ast.Import):
                s = i
                break
        for i, c in enumerate(self.body[s:]):
            if not isinstance(c.node, (ast.Import, ast.ImportFrom)):
                e = s + i
                break

        # PREAMBLE
        for c in self.body[:s]:
            yield from format(c)

        # TODO: SORT IMPORTS
        for c in self.body[s:e]:
            yield from format(c)

        # EMIT REST
        for c in self.body[e:]:
            yield from format(c)

        yield from emit_comments(self.below_comment)

