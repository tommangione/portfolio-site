import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("a", "Elons site", [], {"href": "x.com"})
        self.assertEqual(node.__repr__(), 'a Elons site   href="x.com" ')

    def test_empty(self):
        node = HTMLNode()
        self.assertEqual(node.__repr__(), "   ")

    def test_prop(self):
        node = HTMLNode("Check my url", "23", [], {"href": "x.com"})
        self.assertEqual(node.props_to_html(), ' href="x.com"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_i(self):
        node = LeafNode("i", "Hello, world!")
        self.assertEqual(node.to_html(), "<i>Hello, world!</i>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), ('<a href="https://www.google.com">'
                                          'Click me!</a>'))

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "example_alt", {"src": "/example/path.jpg"})
        self.assertEqual(node.to_html(), ('<img src="/example/path.jpg" '
                                          'alt="example_alt"/>'))

    def test_node_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), ("<p><b>Bold text</b>Normal text"
                                          + "<i>italic text</i>Normal text"
                                          + "</p>"))

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), ("<div><span>child"
                                                 + "</span></div>"))

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
