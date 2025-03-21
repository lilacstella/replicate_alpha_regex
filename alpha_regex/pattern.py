from alpha_regex import alphabet
import copy

# 1, 0, ☐, ε, ∅, ., ∪, ⋅, *
COST_MAP = {
    "☐": 10,
    "∪": 6,
    "⋅": 5,
    "*": 5,
}

class Pattern:
    def __init__(self, symbol: str = None, members: list['Pattern'] = None):
        if symbol and members:
            raise ValueError("Pattern must be either a symbol or a list of members")
        self.symbol = symbol
        self.members = members
        self.cost = -1

    def __str__(self):
        raise NotImplementedError("Should be implemented by child")

    def __deepcopy__(self, memo={}):
        if memo is None:
            memo = {}
        if self in memo:
            return memo[self]

        if self.symbol:
            memo[self] = Symbol(self.symbol)
        else:
            new_node = self.__class__()
            new_node.members = [copy.deepcopy(member, memo) for member in self.members]
            memo[self] = new_node
        return new_node

    """
    operations
    """
    def __or__(self, other):
        if self.symbol == '∅':
            return other
        if other.symbol == '∅':
            return self

        if self.symbol == 'ε' and other.symbol == 'ε':
            return Symbol.empty_string()

        # if the members consists of the entire alphabet, return any symbol
        if (isinstance(self, Symbol) and self.symbol == '.') or (isinstance(other, Symbol) and other.symbol == '.'):
            return Symbol.any_symbol()

        union = Union(self, other)

        # check if member of this union consists of the entire alphabet
        if all(isinstance(member, Symbol) for member in union.members) and \
            set(member.symbol for member in union.members) == alphabet:
            return Symbol.any_symbol()

        return union

    def __add__(self, other):
        if self.symbol == '∅' or other.symbol == '∅':
            return Symbol.empty_lang()

        if isinstance(self, Star) and isinstance(other, Star):
            if self.members[0].symbol == other.members[0].symbol:
                return self

        return Concatenation(self, other)

    def star(self):
        if self.symbol == '∅':
            return Symbol.empty_lang()
        return Star(self)

    """
    comparison
    """
    def __lt__(self, other):
        """
        Compares the cost of the current tree with another tree.
        :param other: another tree
        :return: True if the current tree has a lower cost than the other tree
        """
        return self.get_cost() < other.get_cost()

    def calculate_cost(self) -> int:
        raise NotImplementedError("Should be implemented by child")

    def get_cost(self) -> int:
        if self.cost == -1:
            self.cost = self.calculate_cost()
        return self.cost


class Union(Pattern):
    def __init__(self, first: Pattern, second: Pattern):
        if isinstance(first, Union):
            members = first.members
        else:
            members = [first]

        if isinstance(second, Union):
            members.extend(second.members)
        else:
            members.append(second)

        # members should be unique
        members = list(set(members))
        super().__init__(members=members)

    def __str__(self):
        # I am trying to make question mark if one of them is epsilon
        if len(self.members) == 2:
            if self.members[0].symbol == 'ε':
                if isinstance(self.members[1], Symbol):
                    return f"{self.members[1]}?"
                return f"({self.members[1]})?"
            if self.members[1].symbol == 'ε':
                if isinstance(self.members[0], Symbol):
                    return f"{self.members[0]}?"
                return f"({self.members[0]})?"
        return f"({'|'.join(str(member) for member in self.members)})"

    def calculate_cost(self) -> int:
        return (len(self.members) - 1) * COST_MAP['∪'] + sum([member.calculate_cost() for member in self.members])


class Concatenation(Pattern):
    def __init__(self, first: Pattern, second: Pattern):
        if isinstance(first, Concatenation):
            first = first.members
        else:
            first = [first]

        if isinstance(second, Concatenation):
            second = second.members
        else:
            second = [second]

        super().__init__(members=first + second)

    def __str__(self):
        # keep all non-ε
        self.members = [member for member in self.members if member.symbol != 'ε']

        return ''.join(str(member) for member in self.members)

    def calculate_cost(self) -> int:
        return (len(self.members) - 1) * COST_MAP['⋅'] + sum([member.calculate_cost() for member in self.members])


class Star(Pattern):
    def __init__(self, first: Pattern):
        super().__init__(members=[first])

    def __str__(self):
        if isinstance(self.members[0], Symbol) or str(self.members[0])[-1] == ')':
            return f"{self.members[0]}*"
        return f"({self.members[0]})*"

    def calculate_cost(self) -> int:
        return COST_MAP['*'] + self.members[0].calculate_cost()


class Symbol(Pattern):
    def __init__(self, symbol: str):
        super().__init__(symbol=symbol)

    def __str__(self):
        return self.symbol

    def calculate_cost(self) -> int:
        return 1

    @staticmethod
    def empty_string():
        return Symbol('ε')

    @staticmethod
    def empty_lang():
        return Symbol('∅')

    @staticmethod
    def any_symbol():
        return Symbol('.')

class Box(Symbol):
    def __init__(self):
        super().__init__(symbol='☐')

    def __str__(self):
        return self.symbol

    def calculate_cost(self) -> int:
        return COST_MAP['☐']
