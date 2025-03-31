from extract_images_and_links import *
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
