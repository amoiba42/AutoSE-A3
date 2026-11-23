import unittest, markdown
E = ["wikilinks"]

class T(unittest.TestCase):
    def test_label(self):
        self.assertEqual(markdown.markdown("[[Release Notes|what is new]]", extensions=E),
                         '<p><a class="wikilink" href="/Release_Notes/">what is new</a></p>')
    def test_whitespace_trimmed(self):
        self.assertEqual(markdown.markdown("[[ a b | the label ]]", extensions=E),
                         '<p><a class="wikilink" href="/a_b/">the label</a></p>')
    def test_plain_unchanged(self):
        self.assertEqual(markdown.markdown("[[Foo]]", extensions=E),
                         '<p><a class="wikilink" href="/Foo/">Foo</a></p>')
    def test_build_url_gets_target_only(self):
        cfg = {"wikilinks": {"base_url": "/w/", "end_url": ".html", "html_class": ""}}
        self.assertEqual(markdown.markdown("[[x y|z]]", extensions=E, extension_configs=cfg),
                         '<p><a href="/w/x_y.html">z</a></p>')
