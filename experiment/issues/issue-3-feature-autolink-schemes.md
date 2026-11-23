**Title:** `<tel:...>` and other scheme autolinks should work wherever `<https://...>` works

`<https://example.com>` becomes a link, including inside a list or next to emphasis. A
`tel:` autolink does not, and stays as a raw tag:

```python
>>> markdown.markdown("- <https://example.com>")
'<ul>\n<li><a href="https://example.com">https://example.com</a></li>\n</ul>'
>>> markdown.markdown("- <tel:+123>")
'<ul>\n<li><tel:+123></li>\n</ul>'
>>> markdown.markdown("*call <tel:+123>*")
'<p><em><tel:+123></em></p>'
```

I'd like `<tel:+123>` to become `<a href="tel:+123">tel:+123</a>` in the same places, while code
spans such as `` `<tel:+123>` `` stay exactly as written, and HTML such as `<span>` keeps working.
