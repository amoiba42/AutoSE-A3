**Title:** Table of contents is useless for my non-English docs

I write documentation in Chinese. The table of contents links don't help me: every heading
seems to get a generic anchor, and I can't tell sections apart. English docs are fine. Can this
be made better?

```python
>>> markdown.markdown("[TOC]\n\n# 你好\n\n# 世界", extensions=["toc"])
```
