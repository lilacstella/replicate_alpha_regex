from regex_node import RegexNode

class RegexTree:
    def __init__(self, root = RegexNode('☐')):
        self.root = root
        self.content = None
        self.cost = -1

    def __str__(self):
        return self.root.print_tree()

    def __lt__(self, other):
        return self.get_cost() < other.get_cost()

    def get_cost(self) -> int:
        if self.cost == -1:
            self.cost = self.root.calculate_cost()
        return self.cost

    def get_content(self) -> str:
        if not self.content:
            self.content = self.root.interpret_content()
        return self.content

    def get_root(self):
        return self.root