import unittest

from textnode import *
from inline_splitters import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):

    def test_given_case(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])

    def test_bold_only(self):
        text = "This has **bold** text"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 3
        assert nodes[1].text == "bold"
        assert nodes[1].text_type == TextType.BOLD

    def test_italic_only(self):
        text = "This has _italic_ text"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 3
        assert nodes[1].text == "italic"
        assert nodes[1].text_type == TextType.ITALIC

    def test_nested_formats(self):
        text = "**Bold _and italic_**"
        nodes = text_to_textnodes(text)

    def test_empty_text(self):
        text = ""
        nodes = text_to_textnodes(text)
        print(f"Empty text returned: {nodes}")  # Add this line
        assert len(nodes) == 1
        assert nodes[0].text == ""
        assert nodes[0].text_type == TextType.TEXT

    def test_adjacent_formats(self):
        text = "**Bold**_Italic_"
        nodes = text_to_textnodes(text)
        assert len(nodes) == 2
        assert nodes[0].text == "Bold"
        assert nodes[0].text_type == TextType.BOLD
        assert nodes[1].text == "Italic"
        assert nodes[1].text_type == TextType.ITALIC


if __name__ == "__main__":
    unittest.main()

