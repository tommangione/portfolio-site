import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode, HTMLNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node3 = TextNode("This is a text node", TextType.BOLD)
        node4 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node3, node4)

    def test_eq_url(self):
        node5 = TextNode("Check my url", TextType.LINK, "www.example.com")
        node6 = TextNode("Check my url", TextType.LINK, "www.example.com")
        self.assertEqual(node5, node6)

    def test_not_eq_url(self):
        node7 = TextNode("Check my url", TextType.LINK, "www.example1.com")
        node8 = TextNode("Check my url", TextType.LINK, "www.example2.com")
        self.assertNotEqual(node7, node8)

    def test_not_eq_texttype(self):
        node9 = TextNode("Text time", TextType.PLAIN)
        node10 = TextNode("Text time", TextType.ITALIC)
        self.assertNotEqual(node9, node10)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "www.x.com")
        html_node = node.text_node_to_html_node().to_html()
        self.assertEqual(html_node, '<a href="www.x.com">This is a link</a>')

    def test_image(self):
        node = TextNode("alt_text", TextType.IMAGE, "image.com")
        html_node = node.text_node_to_html_node()
        print(html_node)
        html_node = html_node.to_html()
        self.assertEqual(html_node, ('<img src="image.com" alt="alt_text">'))


if __name__ == "__main__":
    unittest.main()
