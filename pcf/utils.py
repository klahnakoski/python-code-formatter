from mo_dots import listwrap, Data
from mo_dots import is_many, is_data
from mo_future import text, decorate
from mo_logs import Log


CR = "\n"


class Sentinal(Data):
    """
    HOLD POSITION INFORMATION DURING POST-PARSING
    """


class Previous(Data):
    """
    HOLD THE POSITION OF THE CODE FOUND ABOVE A NODE
    """

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


import ast

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
