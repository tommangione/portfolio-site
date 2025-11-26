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
        if node.text_type == TextType.TEXT or node.text_type == TextType.PLAIN:
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


def extract_markdown_images(text):
    return (re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text))


def extract_markdown_links(text):
    return (re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text))


# both of the next two functions will take an input list of text nodes and
# output a list of nodes with properly formatted links or images

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        p = node.text_type
        if (p == TextType.IMAGE) or (p == TextType.LINK):
            new_nodes.append(node)
        elif node.text == "":
            pass
        elif extract_markdown_images(node.text) == []:
            new_nodes.append(node)
        else:
            current_text = node.text
            extracted_images = extract_markdown_images(node.text)
            for tuple in extracted_images:
                image_md = f"![{tuple[0]}]({tuple[1]})"
                before, after = current_text.split(image_md, 1)
                if before != "":
                    new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode((tuple[0]),
                                          TextType.IMAGE, tuple[1]))
                current_text = after
            if current_text != "":
                new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        p = node.text_type
        if (p == TextType.IMAGE) or (p == TextType.LINK):
            new_nodes.append(node)
        elif node.text == "":
            pass
        elif extract_markdown_links(node.text) == []:
            new_nodes.append(node)
        else:
            current_text = node.text
            extracted_links = extract_markdown_links(node.text)
            for tuple in extracted_links:
                link_md = f"[{tuple[0]}]({tuple[1]})"
                before, after = current_text.split(link_md, 1)
                if before != "":
                    new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode((tuple[0]), TextType.LINK, tuple[1]))
                current_text = after
            if current_text != "":
                new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    initial_node = TextNode(text, TextType.PLAIN)
    find_bold = split_nodes_delimiter([initial_node], "**", TextType.BOLD)
    find_italic = split_nodes_delimiter(find_bold, "_", TextType.ITALIC)
    find_code = split_nodes_delimiter(find_italic, "`", TextType.CODE)
    find_images = split_nodes_image(find_code)
    final_list = split_nodes_link(find_images)
    return final_list
