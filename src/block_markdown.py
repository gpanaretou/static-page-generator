from enum import Enum

from htmlnode import HtmlNode, ParentNode
from textnode import TextNode
from inline_markdown import *

class BlockType(Enum):
    heading = '#'
    paragraph = ''
    code = '`'
    quote = '>'
    unordered_list_asterisk = '*'
    unordered_list_dash = '-'
    ordered_list = '.'
    unordered_list = '*-'

def markdown_to_blocks(markdown: str)-> list:
    blocks = markdown.split("\n\n")
    blocks = [x.strip() for x in blocks]
    return blocks

def get_block_type(block: str)-> str:
    first_char = block[0]
    
    if first_char == BlockType.heading.value:
        return BlockType.heading.name
    elif first_char == BlockType.quote.value:
        return BlockType.quote.name
    elif first_char == BlockType.unordered_list_asterisk.value:
        return BlockType.unordered_list.name
    elif first_char == BlockType.unordered_list_dash.value:
        return BlockType.unordered_list.name
    elif first_char == BlockType.code.value and block[-1] == BlockType.code.value:
        return BlockType.code.name
    elif first_char == BlockType.heading.value:
        return BlockType.heading.name
        
    pattern = r'^\d+\.\s*'

    if bool(re.match(pattern, block)):
        return BlockType.ordered_list.name
    else:
        return BlockType.paragraph.name

def handle_paragraph_block(nodes: list)-> ParentNode:
    parent_node = ParentNode(tag='p', children=nodes)
    return parent_node

def handle_quote_block(nodes: list)-> ParentNode:
    for node in nodes:
        node.value = node.value.strip('> ')

    parent_node = ParentNode(tag='blockquote', children=nodes)
    return parent_node

def handle_code_block(nodes: list)-> ParentNode:
    code_node = ParentNode(tag='code', children=nodes)
    parent_node = ParentNode(tag='pre', children=code_node)
    return parent_node

def handle_ul_node(nodes: list)-> ParentNode:
    for node in nodes:
        node.tag = 'li'
        node.value = node.value.strip('*- ')

    parent_node = ParentNode(tag='ul', children=nodes)
    return parent_node

def handle_ol_node(nodes: list)-> ParentNode:
    pattern = r'^\d+\.\s*'
    for node in nodes:
        node.tag = 'li'
        node.value = re.sub(pattern, '', node.value)

    parent_node = ParentNode(tag='ol', children=nodes)
    return parent_node

# TODO: These handle methods will probably have to change.
# I don't like the way they are rn.
def handle_heading_block(nodes: list)-> list:
    for node in nodes:
        value = node.value
        for i in range(6,0,-1):
            pattern = rf'^\#{{{i}}}\s*'
            if re.match(pattern, value):
                node.tag = f"h{i}"
                break

    return nodes
        

def wrap_node_with_div(html_node: HtmlNode)-> ParentNode:
    parent_node = ParentNode(tag='div', children=html_node)
    return parent_node

def block_to_html(block: str):

    block_type = get_block_type(block)
    html_nodes = []

    text_nodes = []
    for node in block.split('\n'):
        text_nodes.append(text_to_textnodes(node))

    for node in text_nodes:
        html_nodes.append(node[0].text_node_to_html_node())

    if block_type == BlockType.paragraph.name:
        return handle_paragraph_block(html_nodes)
    elif block_type == BlockType.code.name:
        return handle_code_block(html_nodes)
    elif block_type == BlockType.quote.name:
        return handle_quote_block(html_nodes)
    elif block_type == BlockType.unordered_list.name:
        return handle_ul_node(html_nodes)
    elif block_type == BlockType.ordered_list.name:
        return handle_ol_node(html_nodes)
    elif block_type == BlockType.heading.name:
        return handle_heading_block(html_nodes)

def markdown_to_html(markdown: str)-> str:
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        parent_node = block_to_html(block)
        parent_node = wrap_node_with_div(parent_node)
    return parent_node.to_html()