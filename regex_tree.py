from regex_node import RegexNode

class RegexTree:
    """
    Represents a tree of regex nodes. This class is used to represent a regex tree and provide some utility functions.
    This is largely a wrapper around the regex node where the one root is specified and the additional attributes are
    cached.
    """
    def __init__(self, root = RegexNode('☐')):
        """
        Initializes the regex tree with a root node.
        :param root: a regex node that is the root of the tree
        """
        self.root = root
        self.content = None
        self.cost = -1

    def __str__(self):
        """
        Human-readable representation of the tree.
        :return: the human-readable string representation of the tree
        """
        return self.root.print_tree()

    def __lt__(self, other):
        """
        Compares the cost of the current tree with another tree.
        :param other: another tree
        :return: True if the current tree has a lower cost than the other tree
        """
        return self.get_cost() < other.get_cost()

    def get_cost(self) -> int:
        """
        Calculates the cost of the tree and caches it.
        :return: the cost of the tree
        """
        if self.cost == -1:
            self.cost = self.root.calculate_cost()
        return self.cost

    def get_content(self) -> str:
        """
        Interprets the content of the tree and caches it.
        :return: the string representation of the regex
        """
        if not self.content:
            self.content = self.root.interpret_content()
        return self.content

    def get_root(self):
        """
        Returns the root of the tree.
        :return: the root of this tree
        """
        return self.root