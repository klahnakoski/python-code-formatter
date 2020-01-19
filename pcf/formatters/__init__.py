import ast

from pcf import Clause, Group
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
from pcf.formatters.operators import Ins, BoolOp, And, IsNot, Is, BinOp, Add, UnaryOp, USub
from pcf.formatters.passes import Pass
from pcf.formatters.returns import Return
from pcf.formatters.subscript import Subscript
from pcf.formatters.tries import Try
from pcf.formatters.tuple import Tuple
from pcf.formatters.whiles import While

lookup = {
    Clause: Clause,
    Group: Group,
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
