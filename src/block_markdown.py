from enum import Enum

from htmlnode import HtmlNode, ParentNode
from textnode import TextNode
from inline_markdown import *

class BlockType(Enum):
    heading = '#'
    paragraph = ''
    code = '```'
    quote = '>'
    unordered_list_asterisk = '*'
    unordered_list_dash = '-'
    ordered_list = '.'
    unordered_list = '*-'

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [x.strip() for x in blocks]
    return blocks

def block_to_block_type(block):
    first_char = block[0]
    
    if first_char == BlockType.heading.value:
        return BlockType.heading.name
    elif first_char == BlockType.quote.value:
        return BlockType.quote.name
    elif first_char == BlockType.unordered_list_asterisk.value:
        return BlockType.unordered_list.name
    elif first_char == BlockType.unordered_list_dash.value:
        return BlockType.unordered_list.name
    
    # check if it is code block
    if len(block) < len(2 * BlockType.code.value):
        if block[:3] == block[-3:] and block[:3] == BlockType.code.value:
            return BlockType.code.name
        
    second_char = block[1]
    lines = block.split('\n')

    if second_char == BlockType.ordered_list.value and first_char == '1':
        for i, line in enumerate(lines, start=1):
            if line[0] != str(i) or line[1] != BlockType.ordered_list.value:
                return BlockType.paragraph.name
        return BlockType.ordered_list.name
    else:
        return BlockType.paragraph.name

def handle_paragraph_block(block, nodes: list):
    parent_node = ParentNode(tag='p', children=nodes)
    return parent_node

def handle_quote_block(block, nodes: list):
    parent_node = ParentNode(tag='blockquote', children=nodes)
    return parent_node

def wrap_node_with_div(html_node):
    parent_node = ParentNode(tag='div', children=html_node)
    return parent_node


def wrap_block_with_appropriate_html_node(block_type: str, block):
    html_nodes = []
    text_nodes = text_to_textnodes(block)

    for node in text_nodes:
        html_nodes.append(node.text_node_to_html_node())

    if block_type == BlockType.paragraph.name:
        return handle_paragraph_block(block, html_nodes)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)

        parent_node = wrap_block_with_appropriate_html_node(block_type, block)
        parent_node = wrap_node_with_div(parent_node)
        print(parent_node)

        