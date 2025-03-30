class HTMLNode:
    def __init__(self, tag="", value="", children=[], props={}) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        # return the key value pairs making sure to preserve the spaces between
        for key, value in self.props.items():
            return f" {key}='{value}'"
        return ""

    def __repr__(self) -> str:
        object_string = ""
        object_string += self.tag
        object_string += self.value
        if self.children:
            object_string += " ".join(self.children)
        object_string += str(self.props)
        return object_string


class LeafNode(HTMLNode):
    def __init__(self, tag, value, children=[], props={}) -> None:
        super().__init__(tag, value, children, props)
        self.children = None
        if not value and tag and tag != "img":
            raise ValueError("Leaf must have a value")
        self.props = props

    def to_html(self):

        if self.tag is None:
            return self.value

        if not self.props:
            return f"<{self.tag}>{self.value}</{self.tag}>"

        props_str = " ".join([f'{key}="{value}"' for key, value in self.props.items()])
        return f"<{self.tag} {props_str}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return super().__repr__()


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props={}) -> None:
        super().__init__(tag, children, props)
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag is required")
        if not self.children:
            raise ValueError("A parent node needs children!")

        # Create opening tag
        # Deal with potential properties
        props_html = ""
        for prop, value in self.props.items():
            props_html += f" {prop}='{value}'"

        html_strings = f"<{self.tag}{props_html}>"

        # Add the html for the children
        for child in self.children:
            html_strings += child.to_html()

        # Add the closing tag

        html_strings += f"</{self.tag}>"

        return html_strings
