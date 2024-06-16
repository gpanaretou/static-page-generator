from textnode import TextType, TextNode
import re

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
        split_text = list(filter(None, split_text))

        if len(split_text) == 1:
            new_nodes.append(TextNode(split_text[0], 'text'))
        else:
            for i in range(0, len(split_text)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_text[i], 'text'))
                else:
                    new_nodes.append(TextNode(split_text[i], text_type))
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode])-> list[TextNode]:
    new_nodes = []

    for node in old_nodes:

        images_list = extract_markdown_images(node.text)
        if node.text == "":
            continue
        elif (node.text_type != TextType.text.name) or (images_list == None):
            new_nodes.append(node)
        else:
            for image in images_list:
                
                splits = node.text.split(f"![{image[0]}]({image[1]})", 1)
                new_nodes.append(TextNode(splits[0], 'text'))
                new_nodes.append(TextNode(image[0], 'image', image[1]))

                new_nodes.extend(split_nodes_image([TextNode(splits[1], 'text')]))
                return new_nodes
            
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode])-> list[TextNode]:
    new_nodes = []

    for node in old_nodes:

        links_list = extract_markdown_links(node.text)
        if node.text == "":
            continue
        elif (node.text_type != TextType.text.name) or (links_list == None):
            new_nodes.append(node)
        else:
            for link in links_list:
                splits = node.text.split(f"[{link[0]}]({link[1]})", 1)
                new_nodes.append(TextNode(splits[0], 'text'))
                new_nodes.append(TextNode(link[0], 'link', link[1]))

                new_nodes.extend(split_nodes_link([TextNode(splits[1], 'text')]))
                return new_nodes
            
    return new_nodes
    
def extract_markdown_images(text: str)-> list[tuple] | None:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    list_of_images = []
    if len(matches) == 0:
        return None
    elif len(matches) == 1:
        return [matches[0],]
    
    for i in range(0, len(matches), 2):
        t = (matches[i], matches[i+1])
        list_of_images.extend(t)

    return list_of_images

def extract_markdown_links(text: str)-> list[tuple] | None:
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)

    list_of_links = []
    if len(matches) == 0:
        return None
    elif len(matches) == 1:
        return [matches[0],]
        
    for i in range(0, len(matches), 2):
        t = (matches[i], matches[i+1])
        list_of_links.extend(t)

    return list_of_links

def text_to_textnodes(text):
    list_of_nodes = [TextNode(text=text, text_type='text')]

    list_of_nodes = split_nodes_delimiter(list_of_nodes, '`', 'code')
    list_of_nodes = split_nodes_delimiter(list_of_nodes, '**', 'bold')
    list_of_nodes = split_nodes_delimiter(list_of_nodes, '*', 'italic')
    list_of_nodes = split_nodes_image(list_of_nodes)
    list_of_nodes = split_nodes_link(list_of_nodes)

    return list_of_nodes