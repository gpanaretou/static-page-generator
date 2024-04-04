from textnode import TextNode
from htmlnode import HtmlNode, LeafNode, ParentNode


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

    print(node.to_html())

    print("\n*** ByE ***")


if __name__ == "__main__":
    main()
