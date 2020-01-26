# python-code-formatter

Python parser that includes comments, with simple formatter

> **Status** - In development, does not work 

## Objective

1. Make a python parser that includes comments
2. Build a Python pretty printer

## Status - Failure

Jan2020 - It appears the python `ast` output is inadequate to build a comment parser on top: The ast tokens do not have the necessary resolution; many structures are missing source references (like `lineno`). I had thought that adding `before` and `after` structures to what existed would be enough, but large structures like `ast.ImportFrom` have substructures containing comments and no source references. If this project was to be successful, then we must "parse" those additional structures, name them, and provide formatting functions for them.  Even so, I am not certain how big a task this will end up being.  

It is probably easier to make a Python PEG parser from scratch; with a little meta-programming to  attach the comments to the nodes.

## Motivation

Black has a nice design philosophy: *Don't complain, just fix the code.*  I like this philosphy, but I do not like some of Black's formatting decisions; generally around how little code it puts on a line.  I attempted to change the code, but the formatting algorithms are weaved into the datastructures and algorithms used to manipulate the code: It looks like Black's formatting choices were a side effect of it's internal data structures rather than anything from a higher moral plane.

This code formatter will be split into two parts: The parser and the pretty printer. With separation comes flexibility: The parser will provide an AST, that can be used with any number of other pretty printers. With a full parse tree, we provide more context to format code. 

## Strategy

Use the Python `ast` module to parse Python. Since the `ast` nodes ignore many structural code elements that are important to properly placing comments, a second pass annotates the nodes with comments and any `previous.code` found in the source file. 

All ast nodes annotated by wrapping them in [Data](https://github.com/klahnakoski/mo-dots/blob/dev/README.md#overview) with the following parameters:

* `node` - point to original ast node
* `before_comment` - (optional) list of strings with lines found above `node`
* `line_comment` - (optional) string holding comment on this' `node` line
* `previous` - (optional) points to code above this node, and is just-another-node
* `previous.code` - code above `node`, and not in the `ast`: For example `else:`, `(`, `[`, etc
* `previous.before_comment` - (optional) list of strings found above the `code`
* `previous.line_comment` - (optional) string found to the right of the `code`

Here is an example of code with two nodes `test` and `body[0]`, and all the possible comment locations. The surrounding nodes have not been included for simplicity.:

```python
             # test.previous.before_comment 
if (         # test.previous.line_comment
             # test.before_comment  
    test     # test.line_comment
             # body[0].previous.before_comment
):           # body[0].previous.line_comment
             # body[0].before_comment 
    return   # body[0].line_comment
```

As you may presume, `if (` and `):` are code fragments in the source file, but not found in the `ast`.  This makes sense, the `ast` was meant to represent the logical program, and ignore the superficial syntax.

## Success Criterion

Replicate Black functionality by implementing a black pretty printer that passes the Black test suite.  Then we know the parser is robust for other pretty printers. 

