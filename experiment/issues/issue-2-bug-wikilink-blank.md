**Title:** A blank `[[ ]]` disappears when it sits inside emphasis, a table cell or a heading

With the `wikilinks` extension, a wikilink that contains only whitespace vanishes in some places
but not others. `[[]]` is kept as typed everywhere:

```python
>>> markdown.markdown("*see [[]]*", extensions=["wikilinks"])
'<p><em>see [[]]</em></p>'
>>> markdown.markdown("*see [[ ]]*", extensions=["wikilinks"])
'<p><em>see </em></p>'
```

The same thing happens in a table cell (the cell comes out empty) and in a heading with the
`toc` extension (the table of contents gets an empty entry). I'd expect `[[ ]]` to be kept as
typed, just like `[[]]`. Version 3.11.2.
