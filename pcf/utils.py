from mo_dots import listwrap, Data
from pcf.formatters import format


class Clause(Data):
    def format(self):
        yield from emit_comments(self.above_comment)
        yield ":"
        yield from optional_comment(self.line_comment)
        yield from indent_body(self.body)


def format_comment(comment):
    if comment:
        yield "  "
        yield comment
        yield "\n"


def optional_comment(comment):
    if comment:
        yield "  "
        yield comment
    yield "\n"


def filter_none(iter_):
    for i in iter_:
        if i:
            yield i


INDENT = "    "


def emit_lines(body):
    for b in body:
        cr = False
        for i in format(b):
            if i:
                cr = i.endswith("\n")
                yield i
        if not cr:
            yield "\n"


def indent_body(body):
    return indent_lines(emit_lines(body))


def indent_lines(lines):
    indent = INDENT
    for i in lines:
        if i:
            yield indent
            indent = None
            yield i
            if i.endswith("\n"):
                indent = INDENT


def join(body, separator=", "):
    sep = None
    for b in body:
        yield sep
        yield from format(b)
        sep = separator


def emit_comments(lines):
    for l in listwrap(lines):
        yield l
        yield "\n"
