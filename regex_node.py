class RegexNode:
    def __init__(self, value):
        # 1, 0, ☐, ε, ∅, ., ∪, ⋅, *
        self.value: str = value
        self.children: list = []

    def display(self, level=0):
        # represent concat as not just cdot
        value = "," if self.value == "⋅" else self.value
        ret = f"{'\t' * level}{value}\n"
        for child in self.children:
            ret += child.display(level + 1)
        return ret

    def __deepcopy__(self):
        new_node = RegexNode(self.value)
        new_node.children = [child.__deepcopy__() for child in self.children]
        return new_node

    def simplify(self):
        # compresses *
        if self.value == "*" and self.children and self.children[0].value == "*":
            return self.children[0].simplify()
        self.children = [child.simplify() for child in self.children]