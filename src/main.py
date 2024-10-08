import os
import shutil
import pathlib

from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode, ParentNode
from inline_markdown import *
from block_markdown import *


def recursively_copy_directories(src, dst, space=0):
    spaces = space * '  '
    if os.path.isfile(src):
        print(f"{spaces}-> Copying {src} into {dst}")
        shutil.copy(src, dst)
        return

    for x in os.listdir(src):
        if os.path.isfile(os.path.join(src, x)):
            print(f"{spaces}-> Copying {x} into {dst}")
            shutil.copy(os.path.join(src, x), dst)
        else:
            print(f"{spaces}-> Creating {os.path.join(dst, x)} directory")
            os.mkdir(os.path.join(dst, x))
            recursively_copy_directories(os.path.join(src, x), os.path.join(dst, x), space=space+1)

def copy_from_static_to_public():
    if os.path.exists('static') == False:
        print('Was expecting to find a directory with the name \'static\'.')

    print('------')

    if os.path.exists('public'):
        print('-> Deleting public folder.')
        shutil.rmtree('public')
        print('-> Creating public folder.')
        os.mkdir('public')
    else:
        print('-> Creating public folder.')
        os.mkdir('public')

    recursively_copy_directories(os.path.join('static'), os.path.join('public'))

def extract_title(markdown):
    first = markdown.partition('\n')[0]

    if first.startswith('# '):
        return first.strip('# ')
    else:
        raise Exception("The first line of the markdown file must be a # 1 heading!!")

def generate_page(from_path, template_path, dest_path):

    if not os.path.isdir(os.path.dirname(dest_path)):
        print('-Creating necessary directories for: ', dest_path)
        os.makedirs(os.path.dirname(dest_path))

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as reader:
        markdown_content = reader.read()

    title = extract_title(markdown_content)

    with open(template_path) as reader:
        template_content = reader.read()

    html_content = markdown_to_html(markdown_content)

    template_content = template_content.replace('{{ Title }}', title, 1)
    page_content = template_content.replace('{{ Content }}', html_content, 1)

    # TODO: this should loop all files in the directory
    with open(f"{dest_path}/{from_path.split('/')[-1].split('.')[0]}.html", "w") as html_file:
        html_file.write(page_content)

    return

def generate_pages_recursively(dir_content_path, template_path, dest_dir_path):
    for f in os.listdir(dir_content_path):
        path_from = os.path.join(dir_content_path, f)
        path_to = os.path.join(dest_dir_path)

        if os.path.isfile(path_from):
            generate_page(path_from, template_path, path_to)
        else:
            new_dir_path = os.path.join(path_to, f)
            print('\n')

            if not os.path.isdir(new_dir_path):
                print('-Creating necessary directories for: ', new_dir_path)
                os.makedirs(new_dir_path)

            generate_pages_recursively(path_from, template_path, new_dir_path)
    return




def main():
    print("*** HI ***\n")

    copy_from_static_to_public()
    page = generate_pages_recursively('./content', 'template.html', './public')
    print("\n*** ByE ***")

if __name__ == "__main__":
    main()
