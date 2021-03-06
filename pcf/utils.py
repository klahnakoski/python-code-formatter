import ast

from mo_dots import is_many
from mo_dots import listwrap, Data
from mo_future import text, decorate
from mo_logs import Log

SPACE = " "
DOUBLE_SPACE = "  "
INDENT = "    "
CR = "\n"


class Sentinal(Data):
    """
    HOLD POSITION INFORMATION DURING POST-PARSING
    """

    pass



class Formatter:
    def format(self):
        raise NotImplemented

    def before_code(self):
        raise NotImplemented

    def is_multiline(self, limit=120):
        """
        :return: True IF THIS NODE IS MANY LINES
        """
        length = 0
        seen_cr = False
        for s in self.format():
            if not s:
                continue
            if seen_cr and s.strip():
                return True  # IF WE SEE NON-WHITESPACE AFTER A CR
            if s is CR:
                seen_cr = True
                length = 0
                continue
            length += len(s)
            if length > limit:
                return True  # LINE IS TOO LONG
        return False

    def all_comments(self):
        """
        EMIT JUST THE COMMENTS
        """
        if not self:
            return
        elif is_many(self):
            for vv in self:
                yield from vv.all_comments()
            return
        elif not isinstance(self, Formatter):
            return

        yield from self.before.before_comment
        yield self.before.line_comment
        yield from self.before_comment
        yield self.line_comment

        for f in self.node._fields:
            v = self[f]
            if not v:
                continue
            elif is_many(v):
                for vv in v:
                    yield from vv.all_comments()
            elif isinstance(v, Formatter):
                yield from v.all_comments()
            else:
                continue

        yield from self.after.before_comment
        yield self.after.line_comment
        yield from self.after_comment


COMMENT_CHECK = True


def extra_comments(formatter):
    """
    EMIT THE before AND after COMMENTS SO formatter NEED NOT
    """

    @decorate(formatter)
    def output(self, before=True):
        if before:
            yield from emit_comments((self.before.before_comment))
            yield from format_comment(self.before.line_comment)
            yield from emit_comments((self.before_comment))

        yield from formatter(self)

        yield from emit_comments((self.after_comment))
        yield from emit_comments((self.after.before_comment))
        yield from format_comment(self.after.line_comment)

    return output


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
        yield DOUBLE_SPACE
        yield comment
        yield CR


def filter_none(iter_):
    fresh_line = True
    whitespace = 0
    for i in iter_:
        if i is CR:
            whitespace = 0
            if fresh_line:
                continue
            else:
                yield CR
                fresh_line = True
        elif not i:
            continue
        elif not i.strip():
            length = len(i)
            if length > whitespace:
                yield i[whitespace:]
            whitespace = length
        else:
            whitespace = 0
            fresh_line = False
            yield i


def emit_lines(body):
    for b in body:
        cr = False
        for i in b.format():
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
        if i is CR and indent is INDENT:
            continue
        if i:
            yield indent
            yield i
            indent = INDENT if i is CR else None


def join(body, separator=", "):
    sep = None
    for b in body:
        yield sep
        yield from b.format()
        sep = separator


def emit_comments(lines):
    for l in listwrap(lines):
        yield CR
        yield l
        yield CR


class Primitive(Data, Formatter):
    """
    FOR NODES THAT LET PARENTS DO FORMATTING
    """

    @format_checker
    @extra_comments
    def format(self):
        return []


class Previous(Data, Formatter):
    """
    HOLD THE POSITION OF THE CODE FOUND ABOVE A NODE
    """

    @format_checker
    @extra_comments
    def format(self):
        # SHOULD NEVER HAPPEN
        raise NotImplemented



from pcf.formatters.assign import Assign
from pcf.formatters.async_function_def import AsyncFunctionDef
from pcf.formatters.async_with import AsyncWith
from pcf.formatters.attribute import Attribute
from pcf.formatters.awaits import Await
from pcf.formatters.call import Call
from pcf.formatters.class_def import ClassDef
from pcf.formatters.compare import Compare
from pcf.formatters.comprehension import Comprehension
from pcf.formatters.constant import Constant
from pcf.formatters.continues import Continue
from pcf.formatters.dict import Dict
from pcf.formatters.expr import Expr
from pcf.formatters.function_def import FunctionDef
from pcf.formatters.ifs import If
from pcf.formatters.import_from import ImportFrom
from pcf.formatters.imports import Import
from pcf.formatters.index import Index
from pcf.formatters.keyword import Keyword
from pcf.formatters.list import List
from pcf.formatters.listcomp import ListComp
from pcf.formatters.module import Module
from pcf.formatters.name import Name
from pcf.formatters.operators import (
    Ins,
    BoolOp,
    And,
    IsNot,
    Is,
    BinOp,
    Add,
    UnaryOp,
    USub,
)
from pcf.formatters.passes import Pass
from pcf.formatters.returns import Return
from pcf.formatters.subscript import Subscript
from pcf.formatters.tries import Try
from pcf.formatters.tuple import Tuple
from pcf.formatters.whiles import While

lookup = {
    Previous: Previous,
    ast.Store: Primitive,
    ast.Load: Primitive,
    ast.AST: Primitive,
    ast.alias: Primitive,
    ast.arguments: Primitive,
    ast.In: Ins,
    ast.BoolOp: BoolOp,
    ast.And: And,
    ast.IsNot: IsNot,
    ast.Is: Is,
    ast.BinOp: BinOp,
    ast.Add: Add,
    ast.UnaryOp: UnaryOp,
    ast.USub: USub,
    ast.Pass: Pass,
    ast.keyword: Keyword,
    ast.Assign: Assign,
    ast.Compare: Compare,
    ast.AsyncFunctionDef: AsyncFunctionDef,
    ast.AsyncWith: AsyncWith,
    ast.Module: Module,
    ast.Import: Import,
    ast.ImportFrom: ImportFrom,
    ast.Expr: Expr,
    ast.Constant: Constant,
    ast.Try: Try,
    ast.FunctionDef: FunctionDef,
    ast.If: If,
    ast.Call: Call,
    ast.ListComp: ListComp,
    ast.comprehension: Comprehension,
    ast.Subscript: Subscript,
    ast.Index: Index,
    ast.While: While,
    ast.Continue: Continue,
    ast.Attribute: Attribute,
    ast.Name: Name,
    ast.Return: Return,
    ast.ClassDef: ClassDef,
    ast.Dict: Dict,
    ast.Await: Await,
    ast.List: List,
    ast.Tuple: Tuple,
}
