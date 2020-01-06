import ast

from mo_logs import Log, strings


class Constant(ast.Constant):

    def format(self):
        value = self.node.value
        if isinstance(value, str):
            if self.is_multiline_string:
                yield '"""' + value + '"""'
            else:
                yield strings.quote(value)
        elif isinstance(value, (float, int)):
            yield str(value)
        elif value is None:
            yield "None"
        elif isinstance(value, type(...)):
            yield "..."
        elif isinstance(value, bytes):
            yield repr(value)
        else:
            Log.error(
                "do not know how to handle {{type}}", type=value.__class__.__name__
            )

