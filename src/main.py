from textnode import TextNode
from htmlnode import HtmlNode, LeafNode, ParentNode

from enum import Enum

class TextType(Enum):
    text = ''
    bold = '**'
    italic = '*'
    code = '`'
    link = ''
    image = ''

def text_node_to_html_node(text_node):
    text_type = text_node.text_type

    if text_type not in TextType.__members__.keys():
        raise ValueError(f"{text_type} is not supported!")

    if text_type == TextType.text.name:
        return LeafNode(value=text_node.text)
    if text_type == TextType.bold:
        return LeafNode(tag="b", value=text_node.text)
    if text_type == TextType.italic:
        return LeafNode(tag="i", value=text_node.text)
    if text_type == TextType.code:
        return LeafNode(tag="code", value=text_node.text)
    if text_type == TextType.link:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    if text_type == TextType.image:
        return LeafNode(tag="img", value="", props={"src": text_node.url,
                                                    "alt": text_node.text})

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: str) -> list:
    new_nodes = []
    
    if (delimiter == '`' and text_type is not TextType.code.name) or \
        (delimiter == '**' and text_type is not TextType.bold.name) or \
        (delimiter == '*' and text_type is not TextType.italic.name):
        raise Exception("This delimiter is not supported by Markdown!")

    for node in old_nodes:
        if (node.text_type != TextType.text.name):
            new_nodes.append(node)
            continue

        split_text = node.text.split(f"{delimiter}")
        for text in split_text:
            if text[-1] != ' ':
                new_nodes.append(TextNode(text, text_type))
            else:
                new_nodes.append(TextNode(text, 'text'))
    return new_nodes

def main():
    print("*** HI ***\n")

    node = ParentNode(
        children=[
            ParentNode(
                children=[
                    LeafNode("b", "1-1"),
                ],
                tag="p",
            ),
            LeafNode("b", "1"),
            LeafNode(None, "2"),
            LeafNode("i", "3"),
            LeafNode(None, "4"),
        ],
        tag="p",
    )

    nested_node = ParentNode(
            "p",
            [
                ParentNode(tag='span',
                           children=[LeafNode(None, 'Nested')]),
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

    # print(node.to_html())

    # print(nested_node.to_html())

    text_node = TextNode('test', 'text')
    html_node = text_node_to_html_node(text_node)
    print(html_node)

    node1 = TextNode("This is text with a `code block` word", 'text')
    node2 = TextNode("This is text with a `code block` word", 'text')


    new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.code.name)

    print(new_nodes)
    print("\n*** ByE ***")


if __name__ == "__main__":
    main()
