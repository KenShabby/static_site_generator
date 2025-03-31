import unittest

from split_images_and_links import *
from textnode import TextType, TextNode


class TestSplitLinks(unittest.TestCase):

    def test_split_nodes_link_basic(self):
        node = TextNode("Hello [link text](https://example.com) world", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Hello ")
        self.assertEqual(result[1].text, "link text")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://example.com")
        self.assertEqual(result[2].text, " world")

    def test_split_nodes_link_no_links(self):
        node = TextNode("Just plain text", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Just plain text")

    def test_split_nodes_link_multiple_links(self):
        node = TextNode(
            "Start [first link](https://example.com/1) middle [second link](https://example.com/2) end",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "Start ")
        self.assertEqual(result[1].text, "first link")
        self.assertEqual(result[1].url, "https://example.com/1")
        self.assertEqual(result[2].text, " middle ")
        self.assertEqual(result[3].text, "second link")
        self.assertEqual(result[3].url, "https://example.com/2")
        self.assertEqual(result[4].text, " end")
