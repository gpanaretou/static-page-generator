from enum import Enum

from htmlnode import HtmlNode, ParentNode, LeafNode
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
    elif block[:3] == BlockType.code.value and block[-3:] == BlockType.code.value:
        return BlockType.code.name
        
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

def handle_ul_block(block: str)-> ParentNode:
    li_elements = []
    for line in block.split('\n'):
        text_nodes = text_to_textnodes(line.lstrip('*- '))
        leaf_nodes = []
        for t_node in text_nodes:
            leaf_nodes.append(t_node.text_node_to_html_node())
        li_elements.append(ParentNode(tag='li', children=leaf_nodes))

    ul_element = ParentNode(tag='ul', children=li_elements)
    return ul_element

def handle_ol_block(block: str)-> ParentNode:
    pattern = r'^\d+\.\s*'

    li_elements = []
    for line in block.split('\n'):
        line = re.sub(pattern, '', line)
        text_nodes = text_to_textnodes(line)
        leaf_nodes = []
        for t_node in text_nodes:
            leaf_nodes.append(t_node.text_node_to_html_node())
        li_elements.append(ParentNode(tag='li', children=leaf_nodes))

    ol_element = ParentNode(tag='ol', children=li_elements)
    return ol_element

# TODO: These handle methods will probably have to change.
# I don't like the way they are rn.
def handle_heading_block(block: str)-> ParentNode:
    h_order = 0
    for heading_order in range(6,0,-1):
        if block[:heading_order] == (BlockType.heading.value * heading_order):
            h_order = heading_order
            break
    
    block = block.strip('# ')
    t_nodes = text_to_textnodes(block)

    html_nodes = []
    for t in t_nodes:
        html_nodes.append(t.text_node_to_html_node())

    p_node = ParentNode(tag=f"h{h_order}", children=html_nodes)
    return p_node
        

def wrap_node_with_div(html_node: HtmlNode)-> ParentNode:
    parent_node = ParentNode(tag='div', children=html_node)
    return parent_node

def block_to_html(block: str):

    block_type = get_block_type(block)
    html_nodes = []

    # each condition should be its own unit tested method
    if block_type == BlockType.code.name:
        text_node = TextNode(text=block.lstrip('`').rstrip('`'), text_type='text')
        html_nodes.append(text_node.text_node_to_html_node())
    elif block_type == BlockType.heading.name:
        return handle_heading_block(block)
    elif block_type == BlockType.ordered_list.name:
        return handle_ol_block(block)
    elif block_type == BlockType.unordered_list.name:
        return handle_ul_block(block)
        
    else:
        for node in block.split('\n'):
            text_nodes = text_to_textnodes(node)
            for text_node in text_nodes:
                html_nodes.append(text_node.text_node_to_html_node())

    if block_type == BlockType.paragraph.name:
        return handle_paragraph_block(html_nodes)
    elif block_type == BlockType.code.name:
        return handle_code_block(html_nodes)
    elif block_type == BlockType.quote.name:
        return handle_quote_block(html_nodes)
    elif block_type == BlockType.unordered_list.name:
        return handle_ul_block(html_nodes)

def markdown_to_html(markdown: str)-> str:
    blocks = markdown_to_blocks(markdown)

    list_of_children = []
    ## TODO: this returns a duplicate div as the top level element, fix it
    for block in blocks:
        block_node = block_to_html(block)
        list_of_children.append(block_node)

    parent_node = ParentNode(tag='div', children=list_of_children)
    return parent_node.to_html()