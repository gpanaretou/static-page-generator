from textnode import TextType, TextNode

class InlineMarkdown():

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
                if text[-1] != ' ' and text[0] != ' ':
                    new_nodes.append(TextNode(text, text_type))
                else:
                    new_nodes.append(TextNode(text, 'text'))
        return new_nodes