from textnode import TextNode
from htmlnode import HtmlNode, LeafNode

def main():
    print("*** HI ***\n")
    node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    html_node = HtmlNode(props = {"href": "https://www.google.com", "target": "_blank"})

    print(html_node.props_to_html())
    print(html_node)

    print("-- Leaf node")
    l1_node = LeafNode("This is a paragraph of text.", "p")
    l2_node = LeafNode("Click me!", "a", {"href": "https://www.google.com"})

    print(l1_node.to_html())
    print(l2_node.to_html())
    
    print("-- ")


    print('\n')
    print(node)

    print("\n*** ByE ***")


if __name__ == "__main__":
    main()