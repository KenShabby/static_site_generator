from enum import Enum

import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown) -> BlockType:
    """ Args: A single block of markdown text.
        Returns: A Blocktype enum representing the type of block it is.
    """
    heading_pattern = r"^#{1,6} "
    code_pattern = r"^```.*```$"
    quote_pattern = r"^>"
    unordered_pattern = r"^- "

    # Heading block handling
    match = re.match(heading_pattern, markdown)
    if match:
        return BlockType.HEADING

    # Code block handling
    match = re.search(code_pattern, markdown, re.DOTALL)
    if match:
        return BlockType.CODE

    # Quote block handling
    lines = markdown.split('\n')
    if(all(re.match(quote_pattern, line) for line in lines)):
        return BlockType.QUOTE

    # Unordered list handling
    lines = markdown.split('\n')
    if(all(re.match(unordered_pattern, line) for line in lines)):
        return BlockType.UNORDERED_LIST

    # Ordered list handling
    lines = markdown.split('\n')
    is_ordered_list = True
    expected_number = 1
    
    for line in lines:
        if not line.startswith(f"{expected_number}. "):
            is_ordered_list = False
            break
        expected_number += 1

    if is_ordered_list:
        return BlockType.ORDERED_LIST

    # Paragraph type if nothing else matches
    block_type = BlockType.PARAGRAPH
    return block_type

def markdown_to_blocks(markdown)-> list:
    """Args: Takes a string representing the whole markdown document
    Returns: A list of markdown blocks (text sparated by newlines) of strings
    """

    blocks = [item.strip() for item in markdown.split("\n\n")]
    # Discard empty items
    blocks = [item for item in blocks if item]

   # Normalize internal newlines by handling indentation properly
    normalized_blocks = []
    for block in blocks:
        lines = block.split("\n")
        # Strip each line individually
        lines = [line.strip() for line in lines]
        # Rejoin with single newlines
        normalized_blocks.append("\n".join(lines))

    return normalized_blocks

