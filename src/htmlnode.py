class HtmlNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTML_NODE -> TAG: {self.tag}, VALUE: {self.value}, CHILDREN: {self.children}, PROPS: {self.props}"

    def __eq__(self, node):
        dict1 = self.__dict__
        dict2 = node.__dict__
        if dict1 == dict2:
            return True
        else:
            return False

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props:
            props = []
            for key, value in self.props.items():
                props.append(f' {key}="{value}"')

            return "".join(props)
        else:
            return ""


class LeafNode(HtmlNode):
    def __init__(self, tag=None, value=None, props=None):
        self.tag = tag
        self.value = value
        self.props = props
        super()

    def __repr__(self):
        return f"LEAF_NODE ->TAG: {self.tag}, VALUE: {self.value}, PROPS: {self.props}"

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node requires a value!")

        props = self.props_to_html() if self.props is not None else ''
        tag_opening = f"<{self.tag}{props}>" if self.tag is not None else ''
        tag_closing = f"</{self.tag}>" if self.tag is not None else ''
        return f"{tag_opening}{self.value}{tag_closing}"


class ParentNode(HtmlNode):
    def __init__(self, tag=None, children=None, props=None):
        self.children = children
        self.tag = tag
        self.props = props
        super()

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag cannot be Nil for ParentNode!")
        if self.children is None:
            raise ValueError("A ParentNode must have children!")

        children = self.__connect_children(self.children)

        return f"{children}"

    def __repr__(self):
        return f"PARENT_NODE ->TAG: {self.tag}, CHILDREN: {self.children}, PROPS: {self.props}"

    def __connect_children(self, children):
        tree = []

        tree.append(f"<{self.tag}{self.props_to_html()}>")
        for i in range(len(children)):

            child = children[i]

            if isinstance(child, LeafNode):
                tree.append(child.to_html())
            else:
                tree.append(child.__connect_children(child.children))

        tree.append(f"</{self.tag}>")

        return "".join(tree)
