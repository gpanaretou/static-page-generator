class HtmlNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"TAG: {self.tag}, \nVALUE: {self.value}, \nCHILDREN: {self.children}, \nPROPS: {self.props}"
    
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
                props.append(f" {key}=\"{value}\"")

            return "".join(props)