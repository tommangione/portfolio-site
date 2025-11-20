from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode


class TextType(Enum):
    PLAIN = "plain"
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, TEXT, TEXT_TYPE, URL=None):
        self.text = TEXT
        self.text_type = TEXT_TYPE
        self.url = URL

    def __eq__(self, obj):
        if self.text == obj.text:
            if self.text_type == obj.text_type:
                if self.url == obj.url:
                    return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def text_node_to_html_node(self):
        if self.text_type == TextType.TEXT:
            return LeafNode(None, self.text)
        if self.text_type == TextType.PLAIN:
            return LeafNode("p", self.text)
        if self.text_type == TextType.BOLD:
            return LeafNode("b", self.text)
        if self.text_type == TextType.ITALIC:
            return LeafNode("i", self.text)
        if self.text_type == TextType.CODE:
            return LeafNode("code", self.text)
        if self.text_type == TextType.LINK:
            return LeafNode("a", self.text, {"href": self.url})
        if self.text_type == TextType.IMAGE:
            return LeafNode("img", "", {"src": self.url, "alt": self.text})
        else:
            raise Exception("Unknown TextType")
