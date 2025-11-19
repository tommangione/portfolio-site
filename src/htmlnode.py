class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        # tag - A string representing the HTML tag name
        # (e.g. "p", "a", "h1", etc.)
        # value - A string representing the value of the HTML tag
        # (e.g. the text inside a paragraph)
        # children - A list of HTMLNode objects representing
        # the children of this node
        # props - A dictionary of key-value pairs representing
        # the attributes of the HTML tag.
        # For example, a link (<a> tag) might have
        # {"href": "https://www.google.com"}
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is not None:
            my_dict = self.props
            my_dict_keys = list(my_dict.keys())
            my_dict_values = []
            output_string = " "
            for i in range(len(my_dict_keys)):
                my_dict_values.append(my_dict[my_dict_keys[i]])
            for i in range(len(my_dict_keys)):
                output_string = (output_string + my_dict_keys[i] + '="'
                                 + my_dict_values[i] + '" ')
            return output_string[:-1]
        return ""

    def __repr__(self):
        if self.tag is not None:
            tag_rep = self.tag
        else:
            tag_rep = ""
        if self.value is not None:
            value_rep = self.value
        else:
            value_rep = ""
        if self.children is not None:
            children_rep = ""
            for child in self.children:
                children_rep = children_rep + " " + str(child)
        else:
            children_rep = ""
        if self.props is not None:
            my_dict = self.props
            my_dict_keys = list(my_dict.keys())
            my_dict_values = []
            output_string = " "
            for i in range(len(my_dict_keys)):
                my_dict_values.append(my_dict[my_dict_keys[i]])
            for i in range(len(my_dict_keys)):
                output_string = (output_string
                                 + my_dict_keys[i] + '="'
                                 + my_dict_values[i] + '" ')
            props_rep = output_string
        else:
            props_rep = ""
        return f"{tag_rep} {value_rep} {children_rep} {props_rep}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        elif self.tag == "p":
            return "<p>" + self.value + "</p>"
        elif self.tag == "b":
            return "<b>" + self.value + "</b>"
        elif self.tag == "i":
            return "<i>" + self.value + "</i>"
        elif self.tag == "a" and self.props is not None:
            my_dict = self.props
            return '<a href="' + my_dict["href"] + '">' + self.value + '</a>'
        elif self.tag == "img" and self.props is not None:
            my_dict = self.props
            return ('<img src="' + my_dict["src"]
                    + '" alt="' + self.value + '"/>')
        raise Exception("Reformat to p, b, i, a, or img")


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
