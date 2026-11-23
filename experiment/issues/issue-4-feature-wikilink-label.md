**Title:** Wikilinks: allow a custom label with `[[Target|Label]]`

Right now the link text is always the page name:

```python
>>> markdown.markdown("[[Release Notes]]", extensions=["wikilinks"])
'<p><a class="wikilink" href="/Release_Notes/">Release Notes</a></p>'
```

Most wiki tools let you write `[[Release Notes|what is new]]` so the URL comes from the part
before `|` and the visible text from the part after. Would you add that? Plain `[[Name]]`
should behave exactly as today.
