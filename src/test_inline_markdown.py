import unittest

from inline_markdown import *
from textnode import TextType, TextNode

class TestInlineMarkdown(unittest.TestCase):
    def test_split_node_delimiter_with_bold(self):
        node1 = TextNode("This is text with a **bolded** word", 'text')

        new_nodes = split_nodes_delimiter([node1], "**", TextType.bold.name)

        expected_result = [
            TextNode("This is text with a ", "text"),
            TextNode("bolded", "bold"),
            TextNode(" word", "text"),
        ]


        self.assertEqual(new_nodes, expected_result)

    def test_split_node_delimiter_with_italic(self):
        node1 = TextNode("This is text with a *italic* word", 'text')

        new_nodes = split_nodes_delimiter([node1], "*", TextType.italic.name)

        expected_result = [
            TextNode("This is text with a ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word", "text"),
        ]


        self.assertEqual(new_nodes, expected_result)

    def test_split_node_delimiter_with_code(self):
        node1 = TextNode("This is text with a `code block` word", 'text')

        new_nodes = split_nodes_delimiter([node1], "`", TextType.code.name)

        expected_result = [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
        ]

        self.assertEqual(new_nodes, expected_result)

    def test_split_node_delimiter_with_bad_delimiter(self):
        node1 = TextNode("This is text with a *italic* word", 'text')

        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node1], "**", TextType.italic.name)

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        actual = (extract_markdown_images(text))
        expected = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]

        self.assertEqual(actual, expected)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        actual = extract_markdown_links(text)
        expected =  [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]

        self.assertEqual(actual, expected)

    def test_split_nodes_image(self):
            node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
                'text',
            )
            actual = split_nodes_image([node])
            
            expected = [
                TextNode("This is text with an ", "text"),
                TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and another ", "text"),
                TextNode(
                    "second image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
                ),
            ]

            self.assertEqual(actual, expected)

    def test_split_nodes_link(self):
            node = TextNode(
            "This is text with an [image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
                'text',
            )
            actual = split_nodes_link([node])
            
            expected = [
                TextNode("This is text with an ", "text"),
                TextNode("image", "link", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and another ", "text"),
                TextNode(
                    "second image", "link", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
                ),
            ]

            self.assertEqual(actual, expected)
