#!/usr/bin/env python3
import asyncio
import string
import sys
import unittest
from contextlib import contextmanager
from functools import partial
from io import BytesIO, TextIOWrapper
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, BinaryIO, Generator, List, Tuple, Iterator
from unittest.mock import patch

from black import (
    PY36_VERSIONS,
    DebugVisitor,
    TargetVersion,
    dump_to_file,
    NothingChanged,
    format_file_contents,
    InvalidInput,
    WriteBack,
    main,
)
from click.testing import CliRunner

from mo_files import TempFile
from pcf import format_file_in_place, format_str
from tests.utils import assert_equivalent, assert_stable, FileMode, assert_close_enough

CLOSE_ENOUGH = True


ff = partial(format_file_in_place, mode=FileMode(), fast=True)
fs = partial(format_str, mode=FileMode())
THIS_FILE = Path(__file__)
THIS_DIR = THIS_FILE.parent
EMPTY_LINE = "# EMPTY LINE WITH WHITESPACE" + " (this comment will be removed)"


def dump_to_stderr(*output: str) -> str:
    return "\n" + "\n".join(output) + "\n"


def read_data(name: str, data: bool = True) -> Tuple[str, str]:
    """read_data('test_name') -> 'input', 'output'"""
    if not name.endswith((".py", ".pyi", ".out", ".diff")):
        name += ".py"
    _input: List[str] = []
    _output: List[str] = []
    base_dir = THIS_DIR / "data" if data else THIS_DIR
    with open(base_dir / name, "r", encoding="utf8") as test:
        lines = test.readlines()
    result = _input
    for line in lines:
        line = line.replace(EMPTY_LINE, "")
        if line.rstrip() == "# output":
            result = _output
            continue

        result.append(line)
    if _input and not _output:
        # If there's no output marker, treat the entire file as already pre-formatted.
        _output = _input[:]
    return "".join(_input).strip() + "\n", "".join(_output).strip() + "\n"


@contextmanager
def cache_dir(exists: bool = True) -> Iterator[Path]:
    with TemporaryDirectory() as workspace:
        cache_dir = Path(workspace)
        if not exists:
            cache_dir = cache_dir / "new"
        with patch("CACHE_DIR", cache_dir):
            yield cache_dir


@contextmanager
def event_loop(close: bool) -> Iterator[None]:
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        yield

    finally:
        if close:
            loop.close()


@contextmanager
def skip_if_exception(e: str) -> Iterator[None]:
    try:
        yield
    except Exception as exc:
        if exc.__class__.__name__ == e:
            unittest.skip(f"Encountered expected exception {exc}, skipping")
        else:
            raise


class BlackRunner(CliRunner):
    """Modify CliRunner so that stderr is not merged with stdout.

    This is a hack that can be removed once we depend on Click 7.x"""

    def __init__(self) -> None:
        self.stderrbuf = BytesIO()
        self.stdoutbuf = BytesIO()
        self.stdout_bytes = b""
        self.stderr_bytes = b""
        super().__init__()

    @contextmanager
    def isolation(self, *args: Any, **kwargs: Any) -> Generator[BinaryIO, None, None]:
        with super().isolation(*args, **kwargs) as output:
            try:
                hold_stderr = sys.stderr
                sys.stderr = TextIOWrapper(self.stderrbuf, encoding=self.charset)
                yield output
            finally:
                self.stdout_bytes = sys.stdout.buffer.getvalue()  # type: ignore
                self.stderr_bytes = sys.stderr.buffer.getvalue()  # type: ignore
                sys.stderr = hold_stderr


class BlackTestCase(unittest.TestCase):
    maxDiff = None

    def assertFormatEqual(self, expected: str, actual: str) -> None:
        if not CLOSE_ENOUGH:
            self.assertEqual(expected, actual)
        else:
            assert_close_enough(expected, actual)

    def test_empty(self) -> None:
        source = expected = ""
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_empty_ff(self) -> None:
        expected = ""
        with TempFile() as tmp_file:
            self.assertFalse(ff(tmp_file))
            actual = tmp_file.read()
            self.assertFormatEqual(expected, actual)

    def test_function(self) -> None:
        source, expected = read_data("function")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_function2(self) -> None:
        source, expected = read_data("function2")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_function_trailing_comma(self) -> None:
        source, expected = read_data("function_trailing_comma")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_expression(self) -> None:
        source, expected = read_data("expression")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_pep_572(self) -> None:
        source, expected = read_data("pep_572")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_stable(source, actual, FileMode())
        if sys.version_info >= (3, 8):
            assert_equivalent(source, actual)

    def test_expression_ff(self) -> None:
        source, expected = read_data("expression")
        with TempFile() as tmp_file:
            self.assertTrue(ff(tmp_file))
            actual = tmp_file.read()
            self.assertFormatEqual(expected, actual)
            with patch("dump_to_file", dump_to_stderr):
                assert_equivalent(source, actual)
                assert_stable(source, actual, FileMode())

    def test_fstring(self) -> None:
        source, expected = read_data("fstring")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_pep_570(self) -> None:
        source, expected = read_data("pep_570")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_stable(source, actual, FileMode())
        if sys.version_info >= (3, 8):
            assert_equivalent(source, actual)

    def test_string_quotes(self) -> None:
        source, expected = read_data("string_quotes")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())
        mode = FileMode(string_normalization=False)
        not_normalized = fs(source, mode=mode)
        self.assertFormatEqual(source, not_normalized)
        assert_equivalent(source, not_normalized)
        assert_stable(source, not_normalized, mode=mode)

    def test_slices(self) -> None:
        source, expected = read_data("slices")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_comments(self) -> None:
        source, expected = read_data("comments")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_comments2(self) -> None:
        source, expected = read_data("comments2")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_comments3(self) -> None:
        source, expected = read_data("comments3")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_comments4(self) -> None:
        source, expected = read_data("comments4")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_comments5(self) -> None:
        source, expected = read_data("comments5")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_comments6(self) -> None:
        source, expected = read_data("comments6")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_comments7(self) -> None:
        source, expected = read_data("comments7")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_comment_after_escaped_newline(self) -> None:
        source, expected = read_data("comment_after_escaped_newline")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_cantfit(self) -> None:
        source, expected = read_data("cantfit")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_import_spacing(self) -> None:
        source, expected = read_data("import_spacing")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_composition(self) -> None:
        source, expected = read_data("composition")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_empty_lines(self) -> None:
        source, expected = read_data("empty_lines")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_remove_parens(self) -> None:
        source, expected = read_data("remove_parens")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_string_prefixes(self) -> None:
        source, expected = read_data("string_prefixes")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_numeric_literals(self) -> None:
        source, expected = read_data("numeric_literals")
        mode = FileMode(target_versions=PY36_VERSIONS)
        actual = fs(source, mode=mode)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, mode)

    def test_numeric_literals_ignoring_underscores(self) -> None:
        source, expected = read_data("numeric_literals_skip_underscores")
        mode = FileMode(target_versions=PY36_VERSIONS)
        actual = fs(source, mode=mode)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, mode)

    def test_numeric_literals_py2(self) -> None:
        source, expected = read_data("numeric_literals_py2")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_stable(source, actual, FileMode())

    def test_python2(self) -> None:
        source, expected = read_data("python2")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_python2_print_function(self) -> None:
        source, expected = read_data("python2_print_function")
        mode = FileMode(target_versions={TargetVersion.PY27})
        actual = fs(source, mode=mode)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, mode)

    def test_python2_unicode_literals(self) -> None:
        source, expected = read_data("python2_unicode_literals")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_stub(self) -> None:
        mode = FileMode(is_pyi=True)
        source, expected = read_data("stub.pyi")
        actual = fs(source, mode=mode)
        self.assertFormatEqual(expected, actual)
        assert_stable(source, actual, mode)

    def test_fmtonoff(self) -> None:
        source, expected = read_data("fmtonoff")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_fmtonoff2(self) -> None:
        source, expected = read_data("fmtonoff2")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_remove_empty_parentheses_after_class(self) -> None:
        source, expected = read_data("class_blank_parentheses")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_new_line_between_class_and_code(self) -> None:
        source, expected = read_data("class_methods_new_line")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_bracket_match(self) -> None:
        source, expected = read_data("bracketmatch")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_tuple_assign(self) -> None:
        source, expected = read_data("tupleassign")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_beginning_backslash(self) -> None:
        source, expected = read_data("beginning_backslash")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_deep(self) -> None:
        source, expected = read_data("deep")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_tab_comment_indentation(self) -> None:
        contents_tab = "if 1:\n\tif 2:\n\t\tpass\n\t# comment\n\tpass\n"
        contents_spc = "if 1:\n    if 2:\n        pass\n    # comment\n    pass\n"
        self.assertFormatEqual(contents_spc, fs(contents_spc))
        self.assertFormatEqual(contents_spc, fs(contents_tab))

        contents_tab = "if 1:\n\tif 2:\n\t\tpass\n\t\t# comment\n\tpass\n"
        contents_spc = "if 1:\n    if 2:\n        pass\n        # comment\n    pass\n"
        self.assertFormatEqual(contents_spc, fs(contents_spc))
        self.assertFormatEqual(contents_spc, fs(contents_tab))

        # mixed tabs and spaces (valid Python 2 code)
        contents_tab = "if 1:\n        if 2:\n\t\tpass\n\t# comment\n        pass\n"
        contents_spc = "if 1:\n    if 2:\n        pass\n    # comment\n    pass\n"
        self.assertFormatEqual(contents_spc, fs(contents_spc))
        self.assertFormatEqual(contents_spc, fs(contents_tab))

        contents_tab = "if 1:\n        if 2:\n\t\tpass\n\t\t# comment\n        pass\n"
        contents_spc = "if 1:\n    if 2:\n        pass\n        # comment\n    pass\n"
        self.assertFormatEqual(contents_spc, fs(contents_spc))
        self.assertFormatEqual(contents_spc, fs(contents_tab))

    def test_debug_visitor(self) -> None:
        source, _ = read_data("debug_visitor.py")
        expected, _ = read_data("debug_visitor.out")
        out_lines = []
        err_lines = []

        def out(msg: str, **kwargs: Any) -> None:
            out_lines.append(msg)

        def err(msg: str, **kwargs: Any) -> None:
            err_lines.append(msg)

        with patch("out", out), patch("err", err):
            DebugVisitor.show(source)
        actual = "\n".join(out_lines) + "\n"
        log_name = ""
        if expected != actual:
            log_name = dump_to_file(*out_lines)
        self.assertEqual(
            expected,
            actual,
            f"AST print out is different. Actual version dumped to {log_name}",
        )

    def test_format_file_contents(self) -> None:
        empty = ""
        mode = FileMode()
        with self.assertRaises(NothingChanged):
            format_file_contents(empty, mode=mode, fast=False)
        just_nl = "\n"
        with self.assertRaises(NothingChanged):
            format_file_contents(just_nl, mode=mode, fast=False)
        same = "j = [1, 2, 3]\n"
        with self.assertRaises(NothingChanged):
            format_file_contents(same, mode=mode, fast=False)
        different = "j = [1,2,3]"
        expected = same
        actual = format_file_contents(different, mode=mode, fast=False)
        self.assertEqual(expected, actual)
        invalid = "return if you can"
        with self.assertRaises(InvalidInput) as e:
            format_file_contents(invalid, mode=mode, fast=False)
        self.assertEqual(str(e.exception), "Cannot parse: 1:7: return if you can")

    def test_tricky_unicode_symbols(self) -> None:
        source, expected = read_data("tricky_unicode_symbols")
        actual = fs(source)
        self.assertFormatEqual(expected, actual)
        assert_equivalent(source, actual)
        assert_stable(source, actual, FileMode())

    def test_preserves_line_endings(self) -> None:
        with TemporaryDirectory() as workspace:
            test_file = Path(workspace) / "test.py"
            for nl in ["\n", "\r\n"]:
                contents = nl.join(["def f(  ):", "    pass"])
                test_file.write_bytes(contents.encode())
                ff(test_file, write_back=WriteBack.YES)
                updated_contents: bytes = test_file.read_bytes()
                self.assertIn(nl.encode(), updated_contents)
                if nl == "\n":
                    self.assertNotIn(b"\r\n", updated_contents)

    def test_preserves_line_endings_via_stdin(self) -> None:
        for nl in ["\n", "\r\n"]:
            contents = nl.join(["def f(  ):", "    pass"])
            runner = BlackRunner()
            result = runner.invoke(
                main, ["-", "--fast"], input=BytesIO(contents.encode("utf8"))
            )
            self.assertEqual(result.exit_code, 0)
            output = runner.stdout_bytes
            self.assertIn(nl.encode("utf8"), output)
            if nl == "\n":
                self.assertNotIn(b"\r\n", output)

    def test_assert_equivalent_different_asts(self) -> None:
        with self.assertRaises(AssertionError):
            assert_equivalent("{}", "None")
