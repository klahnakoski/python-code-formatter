import ast
import string
import sys
from enum import Enum
from typing import Union, Iterator

from attr import dataclass, Factory
from black import _fixup_ast_constants, parse_ast, diff
from typed_ast import ast27, ast3

from mo_logs import Log
from pcf import format_str

DEFAULT_LINE_LENGTH = 90
WHITESPACE = string.whitespace


class TargetVersion(Enum):
    PY27 = 2
    PY33 = 3
    PY34 = 4
    PY35 = 5
    PY36 = 6
    PY37 = 7
    PY38 = 8

    def is_python2(self) -> bool:
        return self is TargetVersion.PY27


@dataclass
class FileMode:
    target_versions = Factory(set)
    line_length: int = DEFAULT_LINE_LENGTH
    string_normalization: bool = True
    is_pyi: bool = False

    def get_cache_key(self) -> str:
        if self.target_versions:
            version_str = ",".join(
                str(version.value)
                for version in sorted(self.target_versions, key=lambda v: v.value)
            )
        else:
            version_str = "-"
        parts = [
            version_str,
            str(self.line_length),
            str(int(self.string_normalization)),
            str(int(self.is_pyi)),
        ]
        return ".".join(parts)


PY36_VERSIONS = {TargetVersion.PY36, TargetVersion.PY37, TargetVersion.PY38}


def assert_equivalent(src: str, dst: str) -> None:
    """Raise AssertionError if `src` and `dst` aren't equivalent."""

    def _v(node: Union[ast.AST, ast3.AST, ast27.AST], depth: int = 0) -> Iterator[str]:
        """Simple visitor generating strings to compare ASTs by content."""

        node = _fixup_ast_constants(node)

        yield f"{'  ' * depth}{node.__class__.__name__}("

        for field in sorted(node._fields):
            # TypeIgnore has only one field 'lineno' which breaks this comparison
            type_ignore_classes = (ast3.TypeIgnore, ast27.TypeIgnore)
            if sys.version_info >= (3, 8):
                type_ignore_classes += (ast.TypeIgnore,)
            if isinstance(node, type_ignore_classes):
                break

            try:
                value = getattr(node, field)
            except AttributeError:
                continue

            yield f"{'  ' * (depth+1)}{field}="

            if isinstance(value, list):
                for item in value:
                    # Ignore nested tuples within del statements, because we may insert
                    # parentheses and they change the AST.
                    if (
                            field == "targets"
                            and isinstance(node, (ast.Delete, ast3.Delete, ast27.Delete))
                            and isinstance(item, (ast.Tuple, ast3.Tuple, ast27.Tuple))
                    ):
                        for item in item.elts:
                            yield from _v(item, depth + 2)
                    elif isinstance(item, (ast.AST, ast3.AST, ast27.AST)):
                        yield from _v(item, depth + 2)

            elif isinstance(value, (ast.AST, ast3.AST, ast27.AST)):
                yield from _v(value, depth + 2)

            else:
                yield f"{'  ' * (depth+2)}{value!r},  # {value.__class__.__name__}"

        yield f"{'  ' * depth})  # /{node.__class__.__name__}"

    try:
        src_ast = parse_ast(src)
        dst_ast = parse_ast(dst)

        src_ast_str = "\n".join(_v(src_ast))
        dst_ast_str = "\n".join(_v(dst_ast))
        if src_ast_str != dst_ast_str:
            Log.error("Not the same:\n{{diff|indent}}", diff=diff(src_ast_str, dst_ast_str, "src", "dst"))
    except Exception as e:
        Log.error("Could not compare", cause=e)


def assert_stable(src: str, dst: str, mode: FileMode) -> None:
    """Raise AssertionError if `dst` reformats differently the second time."""
    newdst = format_str(dst, mode=mode)
    if dst != newdst:
        d2 = diff(dst, newdst, "first pass", "second pass")
        Log.error("Not stable DIFF=\n{{d2|indent}}", d2=d2)

def assert_close_enough(expected: str, actual: str) -> None:
    e = 0
    a = 0
    em=len(expected)
    am= len(actual)
    while True:
        while e < em and expected[e] in WHITESPACE:
            e += 1
        while a < am and actual[a] in WHITESPACE:
            a += 1
        if a == am and e == em:
            return  # GOOD ENOUGH
        if actual[a] != expected[e]:
            Log.error(
                "not matching\n{{expected}}\n{{actual}}",
                expected=expected[max(e - 30, 0) : min(e + 30, em)],
                actual=actual[max(a - 30, 0) : min(a + 30, am)],
            )
        e += 1
        a += 1
