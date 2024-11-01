from regex_node import RegexNode

class RegexTree:
    def __init__(self, value: str = None):
        if value is None:
            self.root = None
            self.cost = 0
            self.content = None
            return

        self.root = RegexNode(value)
        self.cost = self.calculate_cost()
        self.content = self.interpret()

    def set_root(self, root: RegexNode):
        self.root = root
        self.cost = self.calculate_cost()
        self.content = self.interpret()

    def display(self):
        return self.root.display()

    def deep_copy(self):
        """
        Deep copy the tree object and returns the root of the new tree
        :return: RegexTree
        """
        new_node = self.root.__deepcopy__()
        new_tree = RegexTree()
        new_tree.set_root(new_node)
        return new_tree

    def interpret(self, node: RegexNode = None):
        if node is None:
            node = self.root
        # if node.value == "☐":
        #     return None

        # interpret empty string
        arr = [self.interpret(child) for child in node.children]
        if None in arr:
            return None

        if node.value == "∪":
            return f"({'|'.join(arr)})"
        if node.value == "⋅":
            return f"({''.join(arr)})"
        if node.value == "*":
            return f"({self.interpret(node.children[0])}*)"

        return node.value

    def calculate_cost(self):
        cost_map = {
            "☐": 10,
            "∪": 6,
            "⋅": 5,
            "*": 5
        }

        def sum_cost(node):
            if not node:
                return 0
            if not node.children: # leaf
                return cost_map.get(node.value, 3)
            if node.value == "*":
                return sum([sum_cost(child) for child in node.children]) + cost_map.get("*")
            return sum([sum_cost(child) for child in node.children]) + cost_map[node.value] * (len(node.children) - 1)

        return sum_cost(self.root)

    def __lt__(self, other):
        return self.cost < other.cost