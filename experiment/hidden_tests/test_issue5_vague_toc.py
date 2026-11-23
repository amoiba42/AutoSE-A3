# Vague issue. Passes for ANY reasonable non-English id scheme: ids must be distinct, must not be
# the generic _1/_2 pattern, and TOC links must point at the heading ids. Exact id text is not checked.
import re, unittest, markdown

IDS = re.compile(r'id="([^"]*)"')

class T(unittest.TestCase):
    def test_cjk_ids_distinct_and_not_generic(self):
        ids = IDS.findall(markdown.markdown("# 你好\n\n# 世界", extensions=["toc"]))
        self.assertEqual(len(ids), 2)
        self.assertEqual(len(set(ids)), 2)
        for i in ids:
            self.assertTrue(i)
            self.assertIsNone(re.fullmatch(r"_\d+", i), i)
    def test_toc_links_match_heading_ids(self):
        out = markdown.markdown("[TOC]\n\n# 你好", extensions=["toc"])
        (heading_id,) = IDS.findall(out.split("</div>")[1])
        self.assertIn(f'href="#{heading_id}"', out)
    def test_ascii_unchanged(self):
        self.assertEqual(markdown.markdown("# Hello World", extensions=["toc"]),
                         '<h1 id="hello-world">Hello World</h1>')
    def test_duplicates_still_unique(self):
        ids = IDS.findall(markdown.markdown("# 你好\n\n# 你好", extensions=["toc"]))
        self.assertEqual(len(set(ids)), 2)
