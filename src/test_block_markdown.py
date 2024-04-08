import unittest

from block_markdown import *

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
                    "1.ordered\n2.list"
                ]
        
        expected = ["quote", "paragraph", "unordered_list", "heading", "ordered_list"]

        for i, block in enumerate(blocks):
            actual = block_to_block_type(block)

            self.assertEqual(expected[i], actual)