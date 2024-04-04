import unittest

from htmlnode import HtmlNode

class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node = HtmlNode()
        node2 = HtmlNode()

        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HtmlNode(props = {"href": "https://www.google.com", "target": "_blank"})
        expected = " href=\"https://www.google.com\" target=\"_blank\""

        props = node.props_to_html()

        self.assertEqual(props, expected)
        
if __name__ == "__main__":
    unittest.main()