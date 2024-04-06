from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    text = 1
    bold = 2
    italic = 3
    code = 4
    link = 5
    image = 6


class TextNode:

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node):
        return self.text == node.text and self.text_type == node.text_type and self.url == node.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

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