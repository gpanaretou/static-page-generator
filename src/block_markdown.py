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

def handle_code_block(block, nodes: list):
    code_node = ParentNode(tag='code', children=nodes)
    parent_node = ParentNode(tag='pre', children=code_node)
    return parent_node

def handle_ul_node(block, nodes: list):
    for node in nodes:
        node.tag = 'li'
        node.value = node.value.strip('*- ')

    parent_node = ParentNode(tag='ul', children=nodes)
    return parent_node

def handle_ol_node(block, nodes: list):
    for node in nodes:
        node.tag = 'li'
        node.value = node.value.strip('*- ')

    parent_node = ParentNode(tag='ol', children=nodes)
    return parent_node  

def wrap_node_with_div(html_node):
    parent_node = ParentNode(tag='div', children=html_node)
    return parent_node


def wrap_block_with_appropriate_html_node(block_type: str, block):
    html_nodes = []

    text_nodes = []
    for node in block.split('\n'):
        text_nodes.append(text_to_textnodes(node))

    for node in text_nodes:
        print(node)
        html_nodes.append(node[0].text_node_to_html_node())

    if block_type == BlockType.paragraph.name:
        return handle_paragraph_block(block, html_nodes)
    elif block_type == BlockType.code.name:
        return handle_code_block(block, html_nodes)
    elif block_type == BlockType.quote.name:
        return handle_quote_block(block, html_nodes)
    elif block_type == BlockType.unordered_list.name:
        return handle_ul_node(block, html_nodes)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    for i, block in enumerate(blocks):
        # print(i, " -> ", block)
        pass

    for block in blocks:
        block_type = block_to_block_type(block)

        parent_node = wrap_block_with_appropriate_html_node(block_type, block)
        parent_node = wrap_node_with_div(parent_node)

        