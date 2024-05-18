import unittest

from block_markdown import *
from htmlnode import LeafNode, ParentNode

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown__to_blocks(self):
        markdown = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
        
        actual = markdown_to_blocks(markdown)

        expected = ['This is **bolded** paragraph',
                    'This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line',
                    "* This is a list\n* with items"]
        
        self.assertEqual(actual, expected)

    def test_block_to_block_type(self):
        blocks = ['>This is **bolded** paragraph',
                    'This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line',
                    "* This is a list\n* with items",
                    "# Heading",
                    "1.ordered\n2.list",
                    "```code block```"
                ]
        
        expected = ["quote", "paragraph", "unordered_list", "heading", "ordered_list", 'code']

        for i, block in enumerate(blocks):
            actual = block_to_block_type(block)

            self.assertEqual(expected[i], actual)

    def test_handle_paragraph_block(self):
        block = "This is a simple block of text"
        nodes = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]

        new_node = handle_paragraph_block(block, nodes)
        expected_node = ParentNode(tag="p", children=nodes)
        self.assertEqual(expected_node, new_node)

    def test_handle_quote_block(self):
        block = ">This is a simple block of text"
        nodes = [
            LeafNode('span', "This is a simple block of text")
        ]

        new_node = handle_quote_block(block, nodes)
        expected_node = ParentNode(tag="blockquote", children=nodes)
        self.assertEqual(expected_node, new_node)

    def test_handle_code_block(self):
        block = "```This is a simple block of text```"
        nodes = [
            LeafNode("code", "This is a simple block of text")
        ]

        new_node = handle_code_block(block, nodes)
        expected_node = ParentNode(tag="pre", children=ParentNode('code', nodes))
        self.assertEqual(expected_node, new_node)

    # def test_handle_ul_node(self):
