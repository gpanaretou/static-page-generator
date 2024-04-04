import unittest

from htmlnode import HtmlNode, LeafNode


class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node = HtmlNode()
        node2 = HtmlNode()

        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HtmlNode(props={"href": "https://www.google.com", "target": "_blank"})
        expected = ' href="https://www.google.com" target="_blank"'

        props = node.props_to_html()

        self.assertEqual(props, expected)


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode(value="test")
        node2 = LeafNode(value="test")

        self.assertEqual(node, node2)

    def test_to_html(self):
        node = LeafNode(
            value="Click me!",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        rawstring = "Click me!"

        self.assertEqual(node.to_html(), rawstring)

        node2 = LeafNode(
            value="Click me!",
            tag="a",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        expected = '<a href="https://www.google.com" target="_blank">Click me!</a>'

        self.assertEqual(node2.to_html(), expected)


if __name__ == "__main__":
    unittest.main()
