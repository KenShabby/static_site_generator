import re

from textnode import *


def split_nodes_image(old_nodes) -> list:
    """Args: Takes a list of TextNodes

    Returns: A list of TextNodes, each list containing the original node broken
    into the respective text, alt_text, and image links.
    """
    new_nodes = []
    for node in old_nodes:
        # If there are no images or links, just return the original TextNode
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        alt_text, url = images[0]
        image_markdown = f"![{alt_text}]({url})"

        # Split the text at this image
        parts = node.text.split(image_markdown, 1)

        # Handle the text before the image
        if parts[0]:
            new_nodes.append(TextNode(parts[0], TextType.TEXT))

        # Create the image node
        new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

        # Create the after text recursively
        if len(parts) > 1 and parts[1]:
            remaining_node = TextNode(parts[1], TextType.TEXT)
            new_nodes.extend(split_nodes_image([remaining_node]))

    return new_nodes


def split_nodes_link(old_nodes) -> list:
    """Args: Takes a list of TextNodes

    Returns: A list of TextNodes, each list containing the original node broken
    into the respective text and url.
    """
    new_nodes = []
    for node in old_nodes:
        # If there are no links, just return the original TextNode
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        text, url = links[0]
        link_markdown = f"[{text}]({url})"

        # Split the text at this image
        parts = node.text.split(link_markdown, 1)

        # Handle the text before the image
        if parts[0]:
            new_nodes.append(TextNode(parts[0], TextType.TEXT))

        # Create the image node
        new_nodes.append(TextNode(text, TextType.LINK, url))

        # Create the after text recursively
        if len(parts) > 1 and parts[1]:
            remaining_node = TextNode(parts[1], TextType.TEXT)
            new_nodes.extend(split_nodes_link([remaining_node]))

    return new_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type) -> list:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text) -> list:
    """Args: Takes raw markdown text. There can be multiple markdown links to
    images in the string.

    Returns: A list of tuples. Each tuple
    contains an alt_text string and a url for the image.
    """

    image_md_regex = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return image_md_regex


def extract_markdown_links(text) -> list:
    """Args: Takes raw markdown text with markdown links.

    Returns: A list of tuples. Each tuple contains the href value and url.
    """

    link_md_regex = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return link_md_regex


def text_to_textnodes(text) -> list:
    """Args: A raw string of Markdown.
    Returns a list of TextNodes
    """
    # Handle the empty string case specifically
    if text == "":
        return [TextNode("", TextType.TEXT)]

    # Apply each splitting method in squence
    nodes = [TextNode(text, TextType.TEXT)]
    # Start with images and links
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    # Move on to the different delimiter types
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes
