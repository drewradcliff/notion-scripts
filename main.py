__version__ = '0.1.0'

import os
import sys
import argparse

from notion.client import NotionClient
from notion.block import TextBlock

def create_text_block(page, text):
    """Creates textblock on page"""
    block = page.children.add_new(TextBlock)
    block.title = text

def delete_all_children(block):
    """Deletes all children in from block"""
    for child in block.children:
        child.remove()

def create_parser():
    """Creates an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('token', help="Obtain the `token_v2` value by inspecting your browser cookies on a logged-in session on Notion.so")
    parser.add_argument('url', help="Notion page url to edit")
    parser.add_argument('property', help="property to move to text block on page")
    return parser

def main(args):
    """Get notion page collection and move specific property to text block"""
    
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    client = NotionClient(token_v2=parsed_args.token)
    page = client.get_block(parsed_args.url)
    
    rows = page.collection.get_rows()
    length = len(rows)

    for count, row in enumerate(rows):
        print(f"moving row ({count+1}/{length})", end='\r')
        row_page = client.get_block(row.id)
        prop = row.get_property(parsed_args.property)
        delete_all_children(row_page)
        create_text_block(row_page, prop)

if __name__ == '__main__':
    main(sys.argv[1:])