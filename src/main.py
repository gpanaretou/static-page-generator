import os
import shutil

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

def main():
    print("*** HI ***\n")

    copy_from_static_to_public()
    
    print("\n*** ByE ***")



if __name__ == "__main__":
    main()
