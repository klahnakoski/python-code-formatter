from mo_dots import listwrap, Data
from mo_dots import is_many, is_data
from mo_future import text, decorate
from mo_logs import Log



CR = "\n"


class Clause(Data):
    def format(self):
        yield from emit_comments(self.above_comment)
        yield ":"
        yield from format_comment(self.line_comment)
        yield CR
        yield from indent_body(self.body)


class Group(Data):
    def format(self):
        yield from emit_comments(self.above_comment)
        yield self.code
        yield from format_comment(self.line_comment)
        yield from format(self.body)


class Formatter:
    def format(self):
        raise NotImplemented

    def previous(self):
        raise NotImplemented

    def all_comments(self):
        """
        EMIT JUST THE COMMENTS
        """
        if not self:
            return
        elif is_many(self):
            for vv in self:
                yield from vv.all_comments
            return
        elif not is_data(self):
            return

        yield from self.previous.above_comment
        yield self.previous.line_comment
        yield from self.above_comment
        yield self.line_comment

        for f in self.node._fields:
            yield from self[f].all_comments()

        yield from self.below_comment


COMMENT_CHECK = True


def format_checker(formatter):
    @decorate(formatter)
    def output(node):
        global COMMENT_CHECK
        if node == None:
            return
        if isinstance(node, str):
            yield node
            return

        comments = node.all_comments()
        for element in formatter(node):
            if element and not isinstance(element, text):
                Log.error("only strings not expected")
            if COMMENT_CHECK and element and element.strip().startswith("#"):
                comment = element
                # WE HAVE A COMMENT
                try:
                    expecting = next(comments)
                    while not expecting or not expecting.strip():
                        expecting = next(comments)
                except StopIteration:
                    expecting = "<EOF>"

                if comment.strip() != expecting.strip():
                    Log.warning(
                        "got\n\t{{comment}}\nexpecting\n\t{{expecting}}",
                        comment=comment,
                        expecting=expecting,
                    )
                    COMMENT_CHECK = False

            yield element
    return output


def format_comment(comment):
    if comment:
        yield "  "
        yield comment
        yield CR


def filter_none(iter_):
    last = CR
    for i in iter_:
        if i is CR and last is CR:
            continue
        if i:
            yield i
            last = i


INDENT = "    "


def emit_lines(body):
    for b in body:
        cr = False
        for i in format(b):
            if i:
                cr = i is CR
                yield i
        if not cr:
            yield CR


def indent_body(body):
    return indent_lines(emit_lines(body))


def indent_lines(lines):
    indent = INDENT
    for i in lines:
        if i:
            yield indent
            yield i
            indent = INDENT if i is CR else None


def join(body, separator=", "):
    sep = None
    for b in body:
        yield sep
        yield from format(b)
        sep = separator


def emit_comments(lines):
    for l in listwrap(lines):
        yield CR
        yield l
        yield CR
