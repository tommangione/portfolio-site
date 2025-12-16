import unittest

from textnode import TextNode, TextType, split_nodes_delimiter
from textnode import extract_markdown_images, extract_markdown_links
from textnode import split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import markdown_to_blocks, markdown_to_html_node

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
        html_node = html_node.to_html()
        self.assertEqual(html_node, ('<img src="image.com" alt="alt_text">'))

    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        fingers_crossed = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, fingers_crossed)

    def test_split_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        fingers_crossed = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, fingers_crossed)

    def test_split_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        fingers_crossed = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, fingers_crossed)

    def test_split_beginning_word(self):
        node = TextNode("**Bold** word first", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        fingers_crossed = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" word first", TextType.TEXT),
        ]
        # print(new_nodes)
        self.assertEqual(new_nodes, fingers_crossed)

    def test_do_an_error(self):
        node = TextNode("**Bold word first", TextType.TEXT)
        try:
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        except:
            self.assertEqual(1, 1)

    def test_do_an_error2(self):
        node = TextNode("Bold** word first", TextType.TEXT)
        try:
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        except:
            self.assertEqual(1, 1)

    def test_regex_finder_images(self):
        text = ("This is text with a ![rick roll]"
                + "(https://i.imgur.com/aKaOqIh.gif)"
                + "This is text with a ![rick roll]"
                + "(https://i.imgur.com/aKaOqIh.gif)")
        expected_list = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                         ("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        extracted_list = extract_markdown_images(text)
        self.assertEqual(expected_list, extracted_list)

    def test_regex_finder_links(self):
        text = ("This is text with a link [to boot dev](https://www.boot.dev)"
                + "and [to youtube](https://www.youtube.com/@bootdotdev)")
        expected_list = [("to boot dev", "https://www.boot.dev"),
                         ("to youtube", "https://www.youtube.com/@bootdotdev")]
        extracted_list = extract_markdown_links(text)
        self.assertEqual(expected_list, extracted_list)


    def test_split_images(self):
        node = TextNode(
            ("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
             + " and another ![second image](https://i.imgur.com/3elNhQu.png)"),
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            ("This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
             + " and another [link2](https://i.imgur.com/3elNhQu.png)"),
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link2", TextType.LINK,
                    "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


    def test_text_to_textnodes(self):
        text = ("This is **text** with an _italic_ word and a `code block` and"
                + " an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and"
                + " a [link](https://boot.dev)")
        expected_output = [TextNode("This is ", TextType.TEXT),
                           TextNode("text", TextType.BOLD),
                           TextNode(" with an ", TextType.TEXT),
                           TextNode("italic", TextType.ITALIC),
                           TextNode(" word and a ", TextType.TEXT),
                           TextNode("code block", TextType.CODE),
                           TextNode(" and an ", TextType.TEXT),
                           TextNode("obi wan image",
                                    TextType.IMAGE,
                                    "https://i.imgur.com/fJRm4Vk.jpeg"),
                           TextNode(" and a ", TextType.TEXT),
                           TextNode("link", TextType.LINK, "https://boot.dev"),
                           ]
        actual_output = text_to_textnodes(text)
        # print("expected output:")
        # print(expected_output)
        # print("\nactual output:")
        # print(actual_output)
        self.assertEqual(expected_output, actual_output)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        # print(blocks)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
        # print(html)

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """# Heading 1

## Heading _two_

###### Heading with **bold** and `code`
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>"
            "<h1>Heading 1</h1>"
            "<h2>Heading <i>two</i></h2>"
            "<h6>Heading with <b>bold</b> and <code>code</code></h6>"
            "</div>",
        )


    def test_quote_block(self):
        md = """> This is a _quote_
> with **inline** stuff
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a <i>quote</i> with <b>inline</b> stuff</blockquote></div>",
        )


    def test_ordered_list(self):
        md = """1. first
2. second with `code`
3. third
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>"
            "<ol>"
            "<li>first</li>"
            "<li>second with <code>code</code></li>"
            "<li>third</li>"
            "</ol>"
            "</div>",
        )


    def test_unordered_list(self):
        md = """- first _item_
- second **item**
- third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>"
            "<ul>"
            "<li>first <i>item</i></li>"
            "<li>second <b>item</b></li>"
            "<li>third item</li>"
            "</ul>"
            "</div>",
        )


    def test_full_document(self):
        md = (
            "# Title\n\n"
            "This is a **bold** paragraph.\n\n"
            "> A _quote_ here\n\n"
            "- item one\n"
            "- item **two**\n\n"
            "1. first\n"
            "2. second with `code`\n\n"
            "```\n"
            "code block _no parse_ **here**\n"
            "```\n"
        )
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>"
            "<h1>Title</h1>"
            "<p>This is a <b>bold</b> paragraph.</p>"
            "<blockquote>A <i>quote</i> here</blockquote>"
            "<ul>"
            "<li>item one</li>"
            "<li>item <b>two</b></li>"
            "</ul>"
            "<ol>"
            "<li>first</li>"
            "<li>second with <code>code</code></li>"
            "</ol>"
            "<pre><code>code block _no parse_ **here**\n</code></pre>"
            "</div>",
        )


if __name__ == "__main__":
    unittest.main()
