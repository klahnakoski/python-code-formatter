import ast
import re

from mo_dots import Null, is_data
from mo_files import File
from mo_future import first
from mo_logs import Log
from pcf.utils import filter_none, CR, Previous, Sentinal, lookup

DEFAULT_LINE_LENGTH = 90


def format_file_in_place(src, mode):
    """Format file under `src` path. Return True if changed.

    If `write_back` is DIFF, write a diff to stdout. If it is YES, write reformatted
    code to the file.
    `mode` and `fast` options are passed to :func:`format_file_contents`.
    """
    file = File(src)
    file.write(format_str(file.read(), mode=mode))
    return True


def format_str(source, mode):
    """Reformat a string and return new contents.
    `mode` determines formatting options, such as how many characters per line are
    allowed.
    """
    lines = source.split(CR)
    head = ast.parse(source)

    def attach_comments(curr, prev):
        """
        LOOK FOR CODE BETWEEN prev AND curr
        :return: wrapped node with the code
        """
        if hasattr(prev.node, "lineno"):
            start_line = i = prev.node.end_lineno - 1
            end_line = curr.node.lineno - 1
            start_col = prev.node.end_col_offset
            end_col = len(lines[start_line]) if start_line < end_line else curr.node.col_offset
            res = lines[start_line][start_col:end_col]
            clr = res.lstrip()

            if prev.node.end_col_offset:
                start_line += 1
                if clr.startswith("#"):
                    prev.line_comment = clr

            while i < end_line:
                if clr and not clr.startswith("#"):
                    break
                i += 1
                start_col = 0  # between-node code is below prev
                res = lines[i]
                clr = res.lstrip()
            else:
                # CHECK OF THERE IS CODE AHEAD OF node ON node's LINE
                res = res[:curr.node.col_offset]
                clr = res.lstrip()
                if not clr:
                    curr.before_comment = [l.strip() for l in lines[start_line:end_line]] or None
                    return

            # IDENTIFY THE CODE
            s = len(res) - len(clr) + start_col
            e = res.find("#")
            if e == -1:
                e = len(res)
            e += start_col
            before = Previous(
                code=lines[i][s:e],
                before_comment=[l.strip() for l in lines[start_line:i]] or None,
                node=ast.AST(
                    **{
                        "lineno": i + 1,
                        "col_offset": s + 1,
                        "end_lineno": i + 1,
                        "end_col_offset": e,
                    }
                ),
            )
            attach_comments(curr, before)
            curr.before = before

    def add_comments(node, prev, parent):
        """
        ANNOTATE node WITH COMMENTS
        :return ANNOTATED node AND ORIGINAL prev
        :param node: THE NODE WE ARE ANNOTATING WITH COMMENTS
        :param prev: THE NODE BEFORE THIS ONE, MAYBE BELONGING TO SOME OTHER STRUCTURE, REQUIRED SO WE CAN ADD IT line_comment
        :param parent: THE PARENT OF node, JUST IN CASE WE WANT MORE CONTEXT
        """
        if not hasattr(node, "_fields"):
            return node, prev
        try:
            wrapper_class = lookup[node.__class__]
            output = wrapper_class(node=node)
        except KeyError:
            Log.error("Do not have a wrapper for class {{class_name}}", class_name=node.__class__.__name__)

        # DECORATORS ARE BEFORE FUNCTION/CLASS DEFINITION
        if "decorator_list" in node._fields:
            dec_list = output["decorator_list"] = []
            for d in node.decorator_list:
                dd, prev = add_comments(d, prev, output)
                dd.is_decorator = True
                dec_list.append(dd)

        # CAPTURE COMMENT LINES ABOVE NODE
        if hasattr(node, "lineno") and hasattr(prev.node, "end_lineno"):
            attach_comments(output, prev)
            first_child = latest_child = Sentinal(  # SENTINEL FOR BEGINNING OF TOKEN
                is_begin=True,
                node={
                    "lineno": node.lineno,
                    "col_offset": node.col_offset,
                    "end_lineno": node.lineno,
                    "end_col_offset": node.col_offset,
                },
            )
        else:
            first_child = latest_child = prev

        for f in node._fields:
            if f == "decorator_list":
                # DECORATORS ARE TREATED SPECIALLY, BEFORE
                continue
            if f == "ctx":
                # THESE "context" VARIABLES HAVE NO PLACE IN THE SOURCE CODE
                continue
            field_value = getattr(node, f)
            if not field_value:
                continue
            if isinstance(field_value, list):
                child_list = output[f] = []
                for c in field_value:
                    cc, latest_child = add_comments(c, latest_child, output)
                    if isinstance(c, ast.Expr):
                        cc.eol = CR
                    child_list.append(cc)
            else:
                value, latest_child = add_comments(
                    field_value, latest_child, output
                )
                output[f] = value
                if isinstance(field_value, ast.Constant) and lines[
                    field_value.lineno - 1
                ][field_value.col_offset :].startswith('"""'):
                    # DETECT MULTILINE STRING
                    value.is_multiline_string = True
                elif isinstance(field_value, ast.arguments) and not any(
                    getattr(field_value, f) for f in field_value._fields
                ):
                    # EMPTY ARGUMENTS HAVE NO LOCATION
                    # ASSUME ARGUMENTS START ON THIS LINE
                    argline = lines[node.lineno - 1]
                    found = re.search(r"\(\s*\)", argline)
                    if not found:
                        Log.error(
                            "expecting empty arguments on line {{line}}", line=argline
                        )
                    location = first(found.regs)
                    latest_child = Sentinal(
                        node={
                            "lineno": node.lineno,
                            "col_offset": location[0] + 1,
                            "end_lineno": node.lineno,
                            "end_col_offset": location[1],
                        }
                    )
                if is_data(value) and value.before:
                    pass
                pass

        prev = latest_child
        if prev is first_child:
            prev = output
        elif hasattr(node, "lineno"):
            # END OF NODE
            eon = ast.AST(
                **{
                    "is_end": True,
                    "lineno": output.node.end_lineno,
                    "col_offset": output.node.end_col_offset,
                    "end_lineno": output.node.end_lineno,
                    "end_col_offset": output.node.end_col_offset,
                }
            )
            eon, _ = add_comments(eon, prev, parent)
            if eon.before.before_comment or eon.before.line_comment:
                output.after = eon.before
            output.after_comment = eon.before_comment

            if not hasattr(prev.node, "lineno"):
                prev = output
            elif (
                (node.end_lineno, node.end_col_offset)
                > (prev.node.end_lineno, prev.node.end_col_offset)
                >= (node.lineno, node.col_offset)
            ):
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

    module = ast.Module(
        _attributes=head._attributes,
        _fields=head._fields,
        body=head.body,
        type_ignores=None,
        lineno=1,
        col_offset=0,
        end_lineno=len(lines),
        end_col_offset=len(lines[-1]),
    )
    module_with_comments, last = add_comments(
        module,
        Sentinal(node={"lineno": 1, "col_offset": 0, "end_lineno": 1, "end_col_offset": 0}),
        Null,
    )
    module_with_comments.node = head
    seq = list(filter_none(module_with_comments.format()))
    new_source = "".join(seq)
    return new_source
