import os
import shutil

from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode, ParentNode
from inline_markdown import *
from block_markdown import *


def rec_traverse_dir(path):
    # if path.
    next

def copy_from_static_to_public():
    if os.path.exists('static'):

        print('------')

        if os.path.exists('public'):
            print('-> Deleting public folder.')
            shutil.rmtree('public')
        else:
            print('-> Creating public folder.')
            os.mkdir('public')

        root_path = 'static'
        dst_root = 'public'

        for x in os.listdir('static'):
            path = os.path.join(root_path, x)
            dst_path = os.path.join(dst_root, x)

            if os.path.isfile(path):
                print(f"-> Copying {path} into {dst_path}")
                shutil.copy(path, dst_path)
            else:
                print("-> Creating {dst_path} directory")
                os.mkdir(dst_path)

        

        

    else:
        print('Was expecting to find a directory with the name \'static\'.')

def main():
    print("*** HI ***\n")

    copy_from_static_to_public()
    
    print("\n*** ByE ***")



if __name__ == "__main__":
    main()
