import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()
