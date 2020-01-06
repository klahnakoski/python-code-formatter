# python-code-formatter

Python parser that includes comments, with simple formatter

> **Status** - In development, does not work 

## Objective

1. Make a python parser that includes comments
2. Build a Python pretty printer


## Motivation

Black has a nice design philosophy: *Don't complain, just fix the code.*  I like this philosphy, but I do not like some of Black's formatting decisions; generally around how little code it puts on a line.  I attempted to change the code, but the formatting algorithms are weaved into the datastructures and algorithms used to manipulate the code: It looks like Black's formatting choices were a side effect of it's internal data structures rather than anything from a higher moral plane.

This code formatter will be split into two parts: The parser and the pretty printer. With separation comes flexibility: The parser will provide an AST, that can be used with any number of other pretty printers. The parser will also provide more context to enable more formatting options than the Black 

## Strategy

Use the Python `ast` module to parse Python. A second pass will annotate the AST nodes with comments:
All ast nodes are wrapped with [Data](https://github.com/klahnakoski/mo-dots/blob/dev/README.md#overview) with the following parameters:

* `node` - point to original ast node
* `above_comment` - (optional) list of strings with lines found above `node`
* `line_comment` - (optional) string holding comment on this' `node` line

Here an example of code that will fill those parameters

```python
# above comment
return a + b  # line comment
```

Code bodies following a colon are wrapped in an extra `Clause` to support the extra comment locations

```python
# above comment
if (  # line comment
    test  
# above comment for clause
):  # line comment for clause
    return
```

All the lines following `):` are contained by the `Clause`.  

## Success Criterion

Replicate Black functionality by implementing a black pretty printer that passes the Black test suite.  Then we know the parser is robust for other pretty printers. 

