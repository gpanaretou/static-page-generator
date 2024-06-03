from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode, ParentNode
from inline_markdown import *
from block_markdown import *


def main():
    print("*** HI ***\n")

    block = "`This is a simple block of text`"

    print(markdown_to_html(block))
    
    print("\n*** ByE ***")



if __name__ == "__main__":
    main()
