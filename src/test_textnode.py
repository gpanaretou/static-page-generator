import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode

class TestTextNote(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")

        self.assertEqual(node, node2)

    def test_text_node_to_html_node_returns_correct_leaf_nodes(self):
        test_cases = [
            TextNode(text="raw text", text_type="text"),
            TextNode(text="raw bold text", text_type="bold"),
            TextNode(text="raw italic text", text_type="italic"),
            TextNode(text="code block", text_type="code"),
            TextNode(text="link text", text_type="link", url="www.google.com"),
            TextNode(text="alt text", url="image.url", text_type="image"),
        ]

        expected_results = [
            LeafNode(value="raw text"),
            LeafNode(value="raw bold text", tag="b"),
            LeafNode(value="raw italic text", tag="i"),
            LeafNode(value="code block", tag="code"),
            LeafNode(value="link text", tag="a", props={"href": "www.google.com"}),
            LeafNode(value="", tag="img", props={"src": "image.url", "alt": "alt text"}),
        ]

        for i in range(len(expected_results)):
            self.assertEqual(expected_results[i], TextNode.text_node_to_html_node(test_cases[i]))


if __name__ == "__main__":
    unittest.main()