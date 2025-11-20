import re
from enum import Enum
from htmlnode import LeafNode


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


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    del_list = ["`", "*", "_"]
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            split_text = node.text.split(delimiter)
            if "" in split_text:
                split_text.remove("")
            if (node.text[0] in del_list) ^ (node.text[-1] in del_list):
                if len(split_text) % 2 == 1:
                    raise Exception("missing delimiter")
                if node.text[0] in del_list:
                    counter = 0
                    for member in split_text:
                        if counter % 2 == 0:
                            type_writer = text_type
                        else:
                            type_writer = TextType.TEXT
                        new_nodes.append(TextNode(member, type_writer))
                        counter += 1
                else:
                    counter = 0
                    for member in split_text:
                        if counter % 2 == 1:
                            type_writer = text_type
                        else:
                            type_writer = TextType.TEXT
                        new_nodes.append(TextNode(member, type_writer))
                        counter += 1
            else:
                if len(split_text) % 2 == 0:
                    raise Exception("missing delimiter")
                counter = 0
                for member in split_text:
                    if counter % 2 == 1:
                        type_writer = text_type
                    else:
                        type_writer = TextType.TEXT
                    new_nodes.append(TextNode(member, type_writer))
                    counter += 1
        else:
            new_nodes.append(node)
    return new_nodes
