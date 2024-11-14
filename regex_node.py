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
    def __init__(self, value: str, left: 'RegexNode' = None, right: 'RegexNode' = None):
        if value not in ['1', '0', '☐', 'ε', '∅', '.', '∪', '⋅', '*']:
            print(f"invalid character for node value {value}")
            exit()

        self.value = value
        self.children = []
        if left:
            self.children.append(left)

        if right:
            self.children.append(right)

    def __deepcopy__(self):
        new_node = RegexNode(self.value)
        new_node.children = [child.__deepcopy__() for child in self.children]
        return new_node

    def calculate_cost(self) -> int:
        if self.value in COST_MAP.keys():
            val = COST_MAP[self.value]
        else:
            val = 1

        return val + sum([child.calculate_cost() for child in self.children])

    def interpret_content(self) -> str:
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
            return f"({''.join(arr)})"
        if self.value == "*":
            return f"({self.children[0].interpret_content()}*)"

        return self.value

    def simplify(self) -> 'RegexNode':
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

def concat(left: RegexNode, right: RegexNode) -> RegexNode:
    return RegexNode('⋅', left, right)

def union(left: RegexNode, right: RegexNode) -> RegexNode:
    return RegexNode('∪', left, right)

def star(node: RegexNode) -> RegexNode:
    return RegexNode('*', node)