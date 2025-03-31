import unittest

from split_images_and_links import *
from textnode import TextType, TextNode


class TestSplitImages(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_image_basic(self):
        node = TextNode(
            "Hello ![alt](https://example.com/image.jpg) world", TextType.TEXT
        )
        result = split_nodes_image([node])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Hello ")
        self.assertEqual(result[1].text, "alt")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "https://example.com/image.jpg")
        self.assertEqual(result[2].text, " world")

    def test_split_nodes_image_no_images(self):
        node = TextNode("Just plain text", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Just plain text")

    def test_split_nodes_image_multiple_images(self):
        node = TextNode(
            "Start ![first](https://example.com/1.jpg) middle ![second](https://example.com/2.jpg) end",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "Start ")
        self.assertEqual(result[1].text, "first")
        self.assertEqual(result[1].url, "https://example.com/1.jpg")
        self.assertEqual(result[2].text, " middle ")
        self.assertEqual(result[3].text, "second")
        self.assertEqual(result[3].url, "https://example.com/2.jpg")
        self.assertEqual(result[4].text, " end")
