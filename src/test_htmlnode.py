import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "<a>", "", None, {"href": "https://www.brendancoen.com", "id": "foo"}
        )
        print(node.props_to_html())
        node2 = HTMLNode("<i>", "node-value", [], {})
        print(node2.props_to_html())

    def test_to_html(self):
        pass

    def test_repr__(self):
        test_repr_node = HTMLNode(
            "<href>", "foobar", [], {"href": "https://www.brendancoen.com", "id": "foo"}
        )
        test_repr_node.__repr__()


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_a_href(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node.__repr__()


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_with_children_of_different_types(self):
        child1 = LeafNode("i", "child1")
        parent1 = ParentNode("a", [child1], {"href": "foo"})
        self.assertEqual(parent1.to_html(), "<a href='foo'><i>child1</i></a>")


if __name__ == "__main__":
    unittest.main()
