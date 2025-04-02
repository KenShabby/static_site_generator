from htmlnode import *
from block_splitters import *
from textnode import *

def markdown_to_html_node(markdown) -> HTMLNode:
    """ Args: Takes a full markdown document.
        Returns: A parent HTML node with child HTML nodes with each nested 
        element.
    """
    # Suggested algorithm:
    # Break the markdown into blocks 
    list_o_blocks = markdown_to_blocks(markdown)

    # Loop over each block
    for block in list_o_blocks:
        # Determine the block type
        block_type = block_to_block_type(block)

        # Based on the type create the proper HTML node with data
        # Assign the proper child HTML node to the block node

        # I created a shared 
    def text_to_children(text) -> list:
        # function that works for 
        # all block types. It takes a string of text and returns a list of 
        # HTMLNodes that represent the inline markdown using previously created 
        # functions (think TextNode -> HTMLNode).

    # The "code" block is a bit of a special case: it should not do any 
    # inline markdown parsing of its children. I didn't use my text_to_children 
    # function for this block type, I manually made a TextNode and used 
    # text_node_to_html_node.

    # Make all the block nodes children under a single parent HTML node (which 
    # should just be a div) and return it.

    return parent_node
