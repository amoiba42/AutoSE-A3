import unittest, markdown

class T(unittest.TestCase):
    def test_emphasis_trailing_space(self):
        self.assertEqual(markdown.markdown("## *Install* ## "), "<h2><em>Install</em></h2>")
    def test_code_trailing_space(self):
        self.assertEqual(markdown.markdown("## Use `x` ## "), "<h2>Use <code>x</code></h2>")
    def test_toc_entry_no_hashes(self):
        out = markdown.markdown("[TOC]\n\n## *Install* ## ", extensions=["toc"])
        self.assertIn('>Install</a>', out)
        self.assertNotIn("##", out)
    def test_unchanged_emphasis(self):
        self.assertEqual(markdown.markdown("## *Install* ##"), "<h2><em>Install</em></h2>")
