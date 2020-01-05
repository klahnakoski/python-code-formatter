import ast
import sys
import tempfile
import traceback
from enum import Enum
from typing import Union, Iterator

from attr import dataclass, Factory
from black import _fixup_ast_constants, parse_ast, diff, format_str
from typed_ast import ast27, ast3

from pcf.formatters import format
from mo_dots import unwraplist, Null, listwrap, Data
from mo_logs import Log, strings

DEFAULT_LINE_LENGTH = 90


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
    except Exception as exc:
        raise AssertionError(
            f"cannot use --safe with this file; failed to parse source file.  "
            f"AST error message: {exc}"
        )

    try:
        dst_ast = parse_ast(dst)
    except Exception as exc:
        log = dump_to_file("".join(traceback.format_tb(exc.__traceback__)), dst)
        raise AssertionError(
            f"INTERNAL ERROR: Black produced invalid code: {exc}. "
            f"Please report a bug on https://github.com/psf/black/issues.  "
            f"This invalid output might be helpful: {log}"
        ) from None

    src_ast_str = "\n".join(_v(src_ast))
    dst_ast_str = "\n".join(_v(dst_ast))
    if src_ast_str != dst_ast_str:
        log = dump_to_file(diff(src_ast_str, dst_ast_str, "src", "dst"))
        raise AssertionError(
            f"INTERNAL ERROR: Black produced code that is not equivalent to "
            f"the source.  "
            f"Please report a bug on https://github.com/psf/black/issues.  "
            f"This diff might be helpful: {log}"
        ) from None


def assert_stable(src: str, dst: str, mode: FileMode) -> None:
    """Raise AssertionError if `dst` reformats differently the second time."""
    newdst = format_str(dst, mode=mode)
    if dst != newdst:
        log = dump_to_file(
            diff(src, dst, "source", "first pass"),
            diff(dst, newdst, "first pass", "second pass"),
        )
        raise AssertionError(
            f"INTERNAL ERROR: Black produced different code on the second pass "
            f"of the formatter.  "
            f"Please report a bug on https://github.com/psf/black/issues.  "
            f"This diff might be helpful: {log}"
        ) from None


def dump_to_file(*output: str) -> str:
    """Dump `output` to a temporary file. Return path to the file."""
    with tempfile.NamedTemporaryFile(
        mode="w", prefix="blk_", suffix=".log", delete=False, encoding="utf8"
    ) as f:
        for lines in output:
            f.write(lines)
            if lines and lines[-1] != "\n":
                f.write("\n")
    return f.name


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
        if i == None:
            continue
        yield i


INDENT = "    "


def emit_lines(body):
    for b in body:
        cr = False
        for l in format(b):
            if l is None:
                continue
            cr = l.endswith("\n")
            yield l
        if not cr:
            yield "\n"


def indent_body(body):
    return indent_lines(emit_lines(body))


def indent_lines(lines):
    please_indent = True
    for i in lines:
        if i == None:
            continue
        if please_indent:
            yield INDENT
            please_indent = False
        yield i
        if i.endswith("\n"):
            please_indent = True


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
