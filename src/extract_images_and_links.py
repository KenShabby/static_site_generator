import re

def extract_markdown_images(text) -> list:
    """ Args: Takes raw markdown text. There can be multiple markdown links to
    images in the string.

    Returns: A list of tuples. Each tuple
    contains an alt_text string and a url for the image.
    """

    image_md_regex = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return image_md_regex


def extract_markdown_links(text) -> list:
    """ Args: Takes raw markdown text with markdown links.

        Returns: A list of tuples. Each tuple contains the href value and url.
    """

    link_md_regex = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return link_md_regex
