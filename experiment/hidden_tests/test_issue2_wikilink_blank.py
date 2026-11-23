import unittest, markdown
W = ["wikilinks"]

class T(unittest.TestCase):
    def test_blank_in_emphasis(self):
        self.assertEqual(markdown.markdown("*see [[ ]]*", extensions=W), "<p><em>see [[ ]]</em></p>")
    def test_blank_in_table_cell(self):
        src = "| a |\n|---|\n| [[ ]] |"
        self.assertIn("<td>[[ ]]</td>", markdown.markdown(src, extensions=W + ["tables"]))
    def test_blank_in_heading_with_toc(self):
        out = markdown.markdown("[TOC]\n\n# [[ ]]", extensions=W + ["toc"])
        self.assertEqual(out.count("[[ ]]"), 2)
    def test_valid_unchanged(self):
        self.assertEqual(markdown.markdown("*see [[x]]*", extensions=W),
                         '<p><em>see <a class="wikilink" href="/x/">x</a></em></p>')
