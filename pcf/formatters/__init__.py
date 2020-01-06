import ast

from mo_logs import Log

lookup = None


def format(node):
    if not lookup:
        _late_import()
    if node == None:
        return
    if isinstance(node, str):
        yield node
        return

    formatter = lookup.get(node.node.__class__)
    if formatter:
        yield from formatter(node)
    else:
        Log.error("Unknown type {{type}}", type=node.node.__class__.__name__)


def _late_import():
    global lookup
    from pcf import Clause
    from pcf.formatters.operators import Ins, BoolOp, And, IsNot, Is, BinOp, Add, UnaryOp, USub
    from pcf.formatters.passes import Pass
    from pcf.formatters.tries import Try
    from pcf.formatters.assign import Assign
    from pcf.formatters.compare import Compare
    from pcf.formatters.async_function_def import AsyncFunctionDef
    from pcf.formatters.async_with import AsyncWith
    from pcf.formatters.attribute import Attribute
    from pcf.formatters.awaits import Await
    from pcf.formatters.call import Call
    from pcf.formatters.listcomp import ListComp
    from pcf.formatters.comprehension import Comprehension
    from pcf.formatters.subscript import Subscript
    from pcf.formatters.index import Index
    from pcf.formatters.whiles import While
    from pcf.formatters.continues import Continue

    from pcf.formatters.class_def import ClassDef
    from pcf.formatters.constant import Constant
    from pcf.formatters.dict import Dict
    from pcf.formatters.list import List
    from pcf.formatters.expr import Expr
    from pcf.formatters.function_def import FunctionDef
    from pcf.formatters.ifs import If
    from pcf.formatters.import_from import ImportFrom
    from pcf.formatters.module import Module
    from pcf.formatters.imports import Import
    from pcf.formatters.name import Name
    from pcf.formatters.returns import Return
    from pcf.formatters.keyword import Keyword

    lookup = {
        Clause: Clause.format,
        ast.In: Ins.format,
        ast.BoolOp: BoolOp.format,
        ast.And: And.format,
        ast.IsNot: IsNot.format,
        ast.Is: Is.format,
        ast.BinOp: BinOp.format,
        ast.Add: Add.format,
        ast.UnaryOp: UnaryOp.format,
        ast.USub: USub.format,

        ast.Pass: Pass.format,
        ast.keyword: Keyword.format,
        ast.Assign: Assign.format,
        ast.Compare: Compare.format,
        ast.AsyncFunctionDef: AsyncFunctionDef.format,
        ast.AsyncWith: AsyncWith.format,
        ast.Module: Module.format,
        ast.Import: Import.format,
        ast.ImportFrom: ImportFrom.format,
        ast.Expr: Expr.format,
        ast.Constant: Constant.format,
        ast.Try: Try.format,
        ast.FunctionDef: FunctionDef.format,
        ast.If: If.format,
        ast.Call: Call.format,
        ast.ListComp: ListComp.format,
        ast.comprehension: Comprehension.format,
        ast.Subscript: Subscript.format,
        ast.Index: Index.format,
        ast.While: While.format,
        ast.Continue: Continue.format,

        ast.Attribute: Attribute.format,
        ast.Name: Name.format,
        ast.Return: Return.format,
        ast.ClassDef: ClassDef.format,
        ast.Dict: Dict.format,
        ast.Await: Await.format,
        ast.List: List.format,
    }
