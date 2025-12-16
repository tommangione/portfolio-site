import re
from enum import Enum
from htmlnode import LeafNode, ParentNode


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
        if self.text_type in (TextType.TEXT, TextType.PLAIN):
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
    for node in old_nodes:
        # leave non-plain/text nodes alone
        if node.text_type not in (TextType.TEXT, TextType.PLAIN):
            new_nodes.append(node)
            continue

        text = node.text
        # if no delimiter in this node, keep it as-is
        if delimiter not in text:
            new_nodes.append(node)
            continue

        parts = text.split(delimiter)

        # even number of parts -> odd number of delimiters -> missing a match
        if len(parts) % 2 == 0:
            raise Exception("missing delimiter")

        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                # outside delimiters: normal text
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # inside delimiters: special type
                new_nodes.append(TextNode(part, text_type))

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


def markdown_to_blocks(markdown):
    output = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        block = block.strip()
        while block[:1] == '\n':
            block = block[1:]
        while block[-1:] == '\n':
            block = block[:-1]
        if block.replace('\n', '').replace('\r', '') != "":
            output.append(block)
    return output


class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"


def block_to_block_type(md_block):
    md_block_lines = md_block.splitlines()
    if md_block[0] == "#":
        return BlockType.heading
    elif md_block[:3] == "```" and md_block[-3:] == "```":
        return BlockType.code
    elif md_block[0] == ">":
        isQuote = True
        for line in md_block_lines:
            if line[0] != ">":
                isQuote = False
        if isQuote:
            return BlockType.quote
    elif md_block[:2] == "- ":
        isUnorderedList = True
        for line in md_block_lines:
            if line[:2] != "- ":
                isUnorderedList = False
        if isUnorderedList:
            return BlockType.unordered_list
    elif md_block_lines[0].split('.')[0].isdigit():
        isOrderedList = True
        for line in md_block_lines:
            if line.split('.')[0].isdigit is False:
                isOrderedList = False
        if isOrderedList:
            return BlockType.ordered_list
    else:
        return BlockType.paragraph


# converts entire document to a single parent HTML node
def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = block_to_html_node(block, block_type)
        children.append(block_node)
    return ParentNode("div", children)


def block_to_html_node(block, block_type):
    if block_type == BlockType.heading:
        output = []
        header_counter = 0
        while block[0] == "#":
            header_counter += 1
            block = block[1:]
        block = block.strip()
        if header_counter > 6:
            header_counter = 6
        textnodes = text_to_textnodes(block)
        for textnode in textnodes:
            entry = textnode.text_node_to_html_node()
            output.append(entry)
        return ParentNode(f"h{header_counter}", output)
    elif block_type == BlockType.code:
        lines = block.splitlines()
        code_text = "\n".join(lines[1:-1]) + "\n"
        code_node = LeafNode("code", code_text)
        return ParentNode("pre", [code_node])
    elif block_type == BlockType.quote:
        output = []
        lines = block.splitlines()
        stripped_lines = [line.lstrip("> ").lstrip(">") for line in lines]
        text = " ".join(stripped_lines)
        textnodes = text_to_textnodes(text)
        for textnode in textnodes:
            entry = textnode.text_node_to_html_node()
            output.append(entry)
        return ParentNode("blockquote", output)
    elif block_type == BlockType.unordered_list:
        output = []
        lines = block.splitlines()
        for line in lines:
            line = line.lstrip("- ")
            nodes = text_to_textnodes(line)
            nodes_html = []
            for node in nodes:
                entry = node.text_node_to_html_node()
                nodes_html.append(entry)
            output.append(ParentNode("li", nodes_html))
        return ParentNode("ul", output)
    elif block_type == BlockType.ordered_list:
        output = []
        lines = block.splitlines()
        for line in lines:
            line = line.split(". ", 1)[1]
            nodes = text_to_textnodes(line)
            nodes_html = []
            for node in nodes:
                entry = node.text_node_to_html_node()
                nodes_html.append(entry)
            output.append(ParentNode("li", nodes_html))
        return ParentNode("ol", output)
    elif block_type == BlockType.paragraph:
        output = []
        block = block.replace("\n", " ")
        textnodes = text_to_textnodes(block)
        for textnode in textnodes:
            entry = textnode.text_node_to_html_node()
            output.append(entry)
        return ParentNode("p", output)
    else:
        raise Exception("Block Type not recognized")
