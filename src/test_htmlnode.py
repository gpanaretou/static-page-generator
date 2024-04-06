import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node = HtmlNode()
        node2 = HtmlNode()

        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HtmlNode(props={"href": "https://www.google.com",
                               "target": "_blank"})
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


class TestParentNode(unittest.TestCase):
    def test_to_html_with_leaf_nodes(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node_html = node.to_html()
        self.assertEqual(node_html, "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_empty_node(self):
        empty_node = ParentNode()
        with self.assertRaises(ValueError):
            empty_node.to_html()

    def test_to_html_with_no_tag(self):
        no_tag_node = ParentNode(tag=None, children='something')
        with self.assertRaises(ValueError):
            no_tag_node.to_html()

    def test_to_html_with_nested_nodes(self):
        nested_node = ParentNode(
            "p",
            [
                ParentNode(tag='span',
                           children=[LeafNode(None, 'Nested')]),
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(nested_node.to_html(), "<p><span>Nested</span><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

if __name__ == "__main__":
    unittest.main()
