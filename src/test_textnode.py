import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node4 = TextNode("This is node four", TextType.CODE)
        node5 = TextNode("This is node five", TextType.LINK, url="www.brendancoen.com")
        self.assertNotEqual(node4, node5)
        node6 = TextNode("Node 6 reporting!", TextType.IMAGE, url="favicon.ico")


if __name__ == "__main__":
    unittest.main()
