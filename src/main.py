from textnode import TextNode
from htmlnode import HtmlNode

def main():
    print("*** HI ***\n")
    node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    html_node = HtmlNode(props = {"href": "https://www.google.com", "target": "_blank"})

    print(html_node.props_to_html())
    print(html_node)
    print(html_node.ex_())

    print('\n')
    print(node)

    print("\n*** ByE ***")


if __name__ == "__main__":
    main()