import unittest

from inline_markdown import InlineMarkdown
from textnode import TextType, TextNode

class TestInlineMarkdown(unittest.TestCase):
    def test_split_node_delimiter_with_bold(self):
        node1 = TextNode("This is text with a **bolded** word", 'text')

        new_nodes = InlineMarkdown.split_nodes_delimiter([node1], "**", TextType.bold.name)

        expected_result = [
            TextNode("This is text with a ", "text"),
            TextNode("bolded", "bold"),
            TextNode(" word", "text"),
        ]


        self.assertEqual(new_nodes, expected_result)

    def test_split_node_delimiter_with_italic(self):
        node1 = TextNode("This is text with a *italic* word", 'text')

        new_nodes = InlineMarkdown.split_nodes_delimiter([node1], "*", TextType.italic.name)

        expected_result = [
            TextNode("This is text with a ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word", "text"),
        ]


        self.assertEqual(new_nodes, expected_result)

    def test_split_node_delimiter_with_code(self):
        node1 = TextNode("This is text with a `code block` word", 'text')

        new_nodes = InlineMarkdown.split_nodes_delimiter([node1], "`", TextType.code.name)

        expected_result = [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
        ]


        self.assertEqual(new_nodes, expected_result)

    def test_split_node_delimiter_with_bad_delimiter(self):
        node1 = TextNode("This is text with a *italic* word", 'text')

        with self.assertRaises(Exception):
            new_nodes = InlineMarkdown.split_nodes_delimiter([node1], "**", TextType.italic.name)
