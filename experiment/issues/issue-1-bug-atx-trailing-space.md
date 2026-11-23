**Title:** Closing `#`s stay in the heading when there is a trailing space and emphasis or code in the title

I write headings in the closed style. When the line ends with a space, the closing hashes
show up in the page, and in the table of contents too:

```python
>>> import markdown
>>> markdown.markdown("## *Install* ##")
'<h2><em>Install</em></h2>'
>>> markdown.markdown("## *Install* ## ")
'<h2><em>Install</em> ##</h2>'
>>> markdown.markdown("## Use `x` ## ", )
'<h2>Use <code>x</code> ##</h2>'
```

With the `toc` extension, the table of contents entry for the trailing-space heading reads
`Install ##` instead of `Install`. I'd expect trailing whitespace to make no difference.
Version 3.11.2.
