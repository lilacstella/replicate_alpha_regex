from alpha_regex import alphabet

# 1, 0, ☐, ε, ∅, ., ∪, ⋅, *
COST_MAP = {
    "☐": 10,
    "∪": 6,
    "⋅": 5,
    "*": 5,
    "(": 0,
    ")": 0,
}

class RegexNode:
    """
    Node for the regex tree, representing a single character or operator
    """
    def __init__(self, value: str, left: 'RegexNode' = None, right: 'RegexNode' = None):
        """
        Initializes the RegexNode, allows for versatile use and defines allowed structures for the tree.

        Checks for whether the value is a valid character or operator, if not it will exit the program.
        :param value: the character or operator
        :param left: potential left child
        :param right: potential right child
        """
        if value not in alphabet.union(['☐', 'ε', '∅', '.', '∪', '⋅', '*']):
            print(f"invalid character for node value {value}")
            exit()

        self.value = value
        self.children = []
        if left:
            self.children.append(left)

        if right:
            self.children.append(right)

    def __deepcopy__(self, memo={}):
        """
        Deep copy the entire tree starting at the current node and its children
        :param memo: memoization dictionary
        :return: returns the new node that will be part of the new cloned tree
        """
        new_node = RegexNode(self.value)
        new_node.children = [child.__deepcopy__(memo) for child in self.children]
        return new_node

    def print_tree(self, level=0):
        """
        Prints the tree in a human-readable format for debug
        The concatenation symbol is represented as a large dot instead of just the cdot symbol for clarity
        :param level: used for internal recursion to keep track of the depth of the indent in string concatenation
        :return: string representation of the tree
        """
        # represent concat as not just cdot
        value = "●" if self.value == "⋅" else self.value
        ret = f"{'\t' * level}{value}\n"
        for child in self.children:
            ret += child.print_tree(level + 1)
        return ret

    def calculate_cost(self) -> int:
        """
        Calculates the cost of the current node and its children. Meant for recursive use
        :return: the cost of the tree with the current node as the root
        """
        if self.value in COST_MAP.keys():
            val = COST_MAP[self.value]
        else:
            val = 1

        return val + sum([child.calculate_cost() for child in self.children])

    def interpret_content(self) -> str:
        """
        Interprets the content of the tree, converting it to a string representation.
        This function does the work of converting the tree representation of a regex into something that's actually used.
        :return: regex representation of the tree with the current node as the root
        """
        # add interpret empty string and empty alphabet
        # empty alphabet means that is just simply won't pass, thus keep it as is?

        arr = [child.interpret_content() for child in self.children]

        if self.value == "∪":
            if self.children[0].value == 'ε':
                return f'({self.children[1].interpret_content()}?)'
            elif self.children[1].value == 'ε':
                return f'({self.children[0].interpret_content()}?)'

            return f"({'|'.join(arr)})"
        if self.value == "⋅":
            if self.children[0].value == 'ε':
                return self.children[1].interpret_content()
            elif self.children[1].value == 'ε':
                return self.children[0].interpret_content()
            
            return f"({''.join(arr)})"
        if self.value == "*":
            return f"({self.children[0].interpret_content()}*)"

        return self.value

    def simplify(self) -> 'RegexNode':
        """
        Simplifies the tree, unnecessary *, and adapting empty string and empty alphabet into proper regex.
        :return:
        """
        # ε, ∅
        if self.value == '*':
            if self.children[0].value == '*':
                return self.children[0].simplify()

        if self.value == '⋅':
            if any(child.value == '∅' for child in self.children):
                return RegexNode('∅')
            if self.children[0].value == 'ε':
                return self.children[1].simplify()
            elif self.children[1].value == 'ε':
                return self.children[0].simplify()

        if self.value == '∪':
            if self.children[0].value == '∅':
                return self.children[1].simplify()
            elif self.children[1].value == '∅':
                return self.children[0].simplify()
            # don't simplify or empty string, it needs to => ?

        simplified = []
        for child in self.children:
            simplified.append(child.simplify())
        self.children = simplified
        return self
