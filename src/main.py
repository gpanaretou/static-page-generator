from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode, ParentNode
from inline_markdown import *
from block_markdown import *


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
    html_node = TextNode.text_node_to_html_node(text_node)
    # print(html_node)

    node1 = TextNode("This is text with a `code block` word", 'text')
    node2 = TextNode("This is text with a `code block` word", 'text')


    text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"

    text = "This is text with an [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and [another link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"


    ul = """ - First item
- Second item
- Third item
- Fourth item"""

    x = markdown_to_html_node(ul)
    print(x)


    print("\n*** ByE ***")


if __name__ == "__main__":
    main()
