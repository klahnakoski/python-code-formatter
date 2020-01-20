import ast

from mo_dots import Data
from pcf.utils import Formatter, format_checker, extra_comments


class Module(Data, Formatter):
    @format_checker
    @extra_comments
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
            yield from c.format()

        # TODO: SORT IMPORTS
        for c in self.body[s:e]:
            yield from c.format()

        # EMIT REST
        for c in self.body[e:]:
            yield from c.format()
