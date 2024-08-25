import unittest

from block_markdown import *
from htmlnode import LeafNode, ParentNode

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
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

    def test_get_block_type(self):
        blocks = ['>This is **bolded** paragraph',
                    'This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line',
                    "* This is a list\n* with items",
                    "# Heading",
                    "1.ordered\n2.list",
                    "```code block```"
                ]
        
        expected = ["quote", "paragraph", "unordered_list", "heading", "ordered_list", 'code']

        for i, block in enumerate(blocks):
            actual = get_block_type(block)

            self.assertEqual(expected[i], actual)

    def test_handle_paragraph_block(self):
        nodes = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]

        new_node = handle_paragraph_block(nodes)
        expected_node = ParentNode(tag="p", children=nodes)
        self.assertEqual(expected_node, new_node)

    def test_handle_quote_block(self):
        nodes = [
            LeafNode('span', "This is a simple block of text")
        ]

        new_node = handle_quote_block(nodes)
        expected_node = ParentNode(tag="blockquote", children=nodes)
        self.assertEqual(expected_node, new_node)

    def test_handle_code_block(self):
        nodes = [
            LeafNode("code", "This is a simple block of text")
        ]

        new_node = handle_code_block(nodes)
        expected_node = ParentNode(tag="pre", children=ParentNode('code', nodes))
        self.assertEqual(expected_node, new_node)

    def test_handle_ul_block(self):
        block = "- Line one\n- Line two"
        new_node = handle_ul_block(block)
        expected_node = ParentNode(tag='ul', children=[
            ParentNode(tag='li', children=[LeafNode(value='Line one')]),
            ParentNode(tag='li', children=[LeafNode(value='Line two')])
        ])
        self.assertEqual(expected_node, new_node)

    def test_handle_ol_block(self):

        block = """1. Dude `Valar` and
2. The tragic saga of the Noldor Elves"""
        new_node = handle_ol_block(block)
        expected_node = ParentNode(tag='ol', children=
                                   [ParentNode(tag='li', children=[
                                                            LeafNode(value='Dude '),
                                                            LeafNode(tag='code', value='Valar'), 
                                                            LeafNode(value=' and')]),
                                   ParentNode(tag='li', children=[LeafNode(value='The tragic saga of the Noldor Elves')])]
                                   )

        self.assertEqual(expected_node, new_node)

    def test_heading_block(self):
        node = "## Heading1 with **bold** text"
        lf = [LeafNode(value='Heading1 with '), LeafNode(tag='b', value='bold'), LeafNode(value=' text')]
        expected = ParentNode(tag="h2", children=lf)
        actual = handle_heading_block(node)

        self.assertEqual(expected, actual)

    def test_wrap_node_with_div(self):
        nodes = [
            LeafNode('li', 'First node'),
            LeafNode('li', 'Second node')
        ]
        new_node = wrap_node_with_div(nodes)
        expected_node = ParentNode('div', nodes)
        self.assertEqual(expected_node, new_node)

    def test_block_to_html_with_paragraph_block(self):
        paragraph_block = "This is the first line\nThis is the second line"
        expected_result = ParentNode(
            'p',
            [LeafNode(value="This is the first line"), LeafNode(value="This is the second line")]
        )

        actual_result = block_to_html(paragraph_block)
        self.assertEqual(expected_result, actual_result)

    def test_block_to_html_with_quote_block(self):
        quote_block = ">This is the first line\n>This is the second line"
        expected_result = ParentNode(
            'blockquote',
            [LeafNode(value="This is the first line"), LeafNode(value="This is the second line")]
        )
        actual_result = block_to_html(quote_block)
        self.assertEqual(expected_result, actual_result)

    def test_block_to_html_with_heading_block(self):
        quote_block = "## H1 **this is** a test"
        expected_result = ParentNode(
            'h2',
            [LeafNode(value="H1 "), LeafNode(tag="b", value="this is"), LeafNode(value=" a test")]
        )
        actual_result = block_to_html(quote_block)
        self.assertEqual(expected_result, actual_result)

    def test_block_to_html_with_code_block(self):
        block = "```This is the first line\nThis is the second line```"
        expected_result = ParentNode(
            'pre',
            ParentNode('code', [LeafNode(value="This is the first line\nThis is the second line")])
        )
        actual_result = block_to_html(block)
        self.assertEqual(expected_result, actual_result)

    def test_block_to_html_with_ul_block(self):
        block = "* This is the first line\n* This is the second line"
        expected_result = ParentNode(
            'ul',
            [LeafNode('li', value="This is the first line"), LeafNode('li', value="This is the second line")]
        )
        actual_result = block_to_html(block)
        self.assertEqual("ul", actual_result.tag)

    def test_block_to_html_with_ol_block(self):
        block = "1. This is the first line\n2. This is the second line"
        expected_result = ParentNode(
            'ol',
            [
                ParentNode(tag='li', children=[LeafNode(value="This is the first line")]), 
                ParentNode(tag='li', children=[LeafNode(value="This is the second line")])
            ]
        )
        actual_result = block_to_html(block)
        self.assertEqual(expected_result, actual_result)

    def test_markdown_to_html(self):
        block = "1. This is the first line\n2. This is the second line"
        result = markdown_to_html(block)
        expected = '<div><ol><li>This is the first line</li><li>This is the second line</li></ol></div>'

        self.assertEqual(expected, result)
    