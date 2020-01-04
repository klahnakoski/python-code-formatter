import ast
import re

from mo_dots import Data, Null
from mo_files import File
from mo_future import first
from mo_logs import Log
from pcf.formatters import format
from pcf.utils import scrub_line, scrub, Clause, filter_none

DEFAULT_LINE_LENGTH = 90


def format_file_in_place(src, mode, *args, **kwargs):
    """Format file under `src` path. Return True if changed.

    If `write_back` is DIFF, write a diff to stdout. If it is YES, write reformatted
    code to the file.
    `mode` and `fast` options are passed to :func:`format_file_contents`.
    """
    file = File(src)
    file.write(format_str(file.read(), mode=mode))
    return True


def format_str(source, mode, *args, **kwargs):
    """Reformat a string and return new contents.
    `mode` determines formatting options, such as how many characters per line are
    allowed.
    """
    lines = source.split("\n")
    head = ast.parse(source)

    def add_comments(node, prev, parent):
        if not hasattr(node, "_fields"):
            return node, prev
        output = Data(node=node)

        # DECORATORS ARE BEFORE FUNCTION/CLASS DEFINITION
        if "decorator_list" in node._fields:
            dec_list = output["decorator_list"] = []
            for d in node.decorator_list:
                dd, prev = add_comments(d, prev, output)
                dd.is_decorator = True
                dec_list.append(dd)

        # CAPTURE COMMENT LINES ABOVE NODE
        if hasattr(node, "lineno") and hasattr(prev.node, "end_lineno"):
            curr_line = node.lineno - 1
            if hasattr(parent.node, "lineno") and parent.node.lineno and lines[parent.node.lineno-1][parent.node.col_offset:][:3] == '"""':
                output.is_multiline_string = True

            if prev.node.end_lineno < node.lineno and prev.node.end_col_offset > 0:
                # GIVE prev.node A LINE COMMENT
                prev.line_comment = scrub_line(
                    lines[prev.node.end_lineno - 1][prev.node.end_col_offset:]
                )
                if prev.line_comment and prev.is_begin:
                    Log.error("logic error")
                # ASSIGN above_comments
                candidate = lines[prev.node.end_lineno : curr_line]
                output.above_clause_comment, output.line_clause_comment, output.above_comment = scrub(
                    candidate
                )
            else:
                # ASSIGN above_comments
                candidate = lines[prev.node.end_lineno - 1 : curr_line]
                output.above_clause_comment, output.line_clause_comment, output.above_comment = scrub(
                    candidate
                )

            first_child = latest_child = Data(  # SENTINEL FOR BEGINNING OF TOKEN
                is_begin=True,
                node={
                    "lineno": node.lineno,
                    "col_offset": node.col_offset,
                    "end_lineno": node.lineno,
                    "end_col_offset": node.col_offset,
                }
            )
        else:
            first_child = latest_child = prev

        for f in node._fields:
            if f == "decorator_list":
                continue
            field_value = getattr(node, f)
            if not field_value:
                continue
            if isinstance(field_value, list):
                child_list = output[f] = []
                for c in field_value:
                    cc, latest_child = add_comments(c, latest_child, output)
                    if latest_child.is_begin:
                        Log.error("logic error")
                    child_list.append(cc)
                    # if hasattr(cc.node, "end_lineno") and hasattr(latest_child.node, "end_lineno") and ( cc.node.end_lineno, cc.node.end_col_offset) >= (latest_child.node.end_lineno, latest_child.node.end_col_offset):
                    #     latest_child = cc

                if child_list:
                    # WE MAY HAVE HID SOME COMMENTS IN THE FIRST CHILD
                    first_child = child_list[0]
                    if (
                        first_child.above_clause_comment
                        or first_child.line_clause_comment
                    ):
                        output[f] = Data(
                            node=Clause(),
                            body=child_list,
                            above_comment=first_child.above_clause_comment,
                            line_comment=first_child.line_clause_comment,
                        )
            else:
                output[f], latest_child = add_comments(field_value, latest_child, output)
                if (
                        isinstance(field_value, ast.Constant)
                        and lines[field_value.lineno-1][field_value.col_offset:].startswith('"""')
                ):
                    output[f].is_multiline_string = True
                elif isinstance(field_value, ast.arguments) and not any(getattr(field_value, f) for f in field_value._fields):
                    # EMPTY ARGUMENTS HAVE NO LOCATION
                    # ASSUME ARGUMENTS START ON THIS LINE
                    argline = lines[node.lineno-1]
                    found = re.search(r"\(\s*\)", argline)
                    if not found:
                        Log.error("expecting empty arguments on line {{line}}", line=argline)
                    location = first(found.regs)
                    latest_child = Data(node={
                        "lineno": node.lineno,
                        "col_offset": location[0]+1,
                        "end_lineno": node.lineno,
                        "end_col_offset": location[1]
                    })
                pass

        prev = latest_child
        if prev is first_child:
            prev = output
        elif hasattr(node, "lineno"):
            last_child = Data(
                **{
                    "is_end": True,
                    "lineno": output.node.end_lineno,
                    "col_offset": output.node.end_col_offset,
                    "end_lineno": output.node.end_lineno,
                    "end_col_offset": output.node.end_col_offset,
                }
            )
            add_comments(last_child, latest_child, parent)
            output.below_comments = last_child.above_comments

            if not hasattr(prev.node, "lineno"):
                prev = output
            elif (node.end_lineno, node.end_col_offset) > (prev.node.end_lineno, prev.node.end_col_offset) >= (node.lineno, node.col_offset):
                # IF THE output CONTAINS THE prev, THEN ASSUME THE output IS prev
                eol = Data(
                    **{
                        "is_end": True,
                        "lineno": output.node.end_lineno,
                        "col_offset": output.node.end_col_offset,
                        "end_lineno": output.node.end_lineno,
                        "end_col_offset": output.node.end_col_offset,
                    }
                )
                add_comments(eol, prev, parent)
                output.below_comments = eol.above_comments
                prev = output
            elif (
                # IF ALL ON ONE LINE, THEN GIVE COMMENT TO BIGGEST ast ON LINE
                node.lineno
                == node.end_lineno
                == prev.node.lineno
                == prev.node.end_lineno
            ):
                prev = output

        return output, prev

    module = Data(
        _attributes=head._attributes,
        _fields=head._fields,
        body=head.body,
        lineno=1,
        col_offset=0,
        end_lineno=len(lines),
        end_col_offset=len(lines[-1]),
    )
    module_with_comments, last = add_comments(
        module,
        Data(node={"lineno": 1, "col_offset": 0, "end_lineno": 1, "end_col_offset": 0}),
        Null
    )
    module_with_comments.node = head
    seq = list(filter_none(format(module_with_comments)))
    new_source = "".join(seq)
    return new_source
