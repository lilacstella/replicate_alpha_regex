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
    """
    should be treated as immutable
    """
    def __init__(self, symbol: str = None, members: list['Pattern'] = None):
        if symbol and members:
            raise ValueError("Pattern must be either a symbol or a list of members")
        self.symbol = symbol
        self.members = members

        # memoized variables
        self._cost = -1
        self._str_cache = None
        self._box_cache = None

    def __str__(self):
        if not self._str_cache:
            self._str_cache = self._compute_str()
        return self._str_cache

    def _compute_str(self):
        raise NotImplementedError("Should be implemented by child")

    """
    search and heuristic functions
    """

    def __deepcopy__(self, memo=None):
        if memo is None:
            memo = {}
        if self in memo:
            return memo[self]

        if isinstance(self, Box):
            memo[self] = Box()
        elif self.symbol:
            memo[self] = Symbol(self.symbol)
        else:
            memo[self] = self.__class__(members=[copy.deepcopy(member, memo) for member in self.members])

        return memo[self]

    def contains_box(self):
        if isinstance(self, Box):
            return True

        if self._box_cache is not None:
            return self._box_cache

        self._box_cache = any(member.contains_box() for member in self.members)
        return self._box_cache

    def simplify(self):
        raise NotImplementedError("Should be implemented by child")

    def replace_all_box(self, replacement: 'Pattern') -> 'Pattern':
        if isinstance(self, Box):
            if self.future:
                return self.future.replace_all_box(replacement)
            return replacement

        if isinstance(self, Symbol):
            return self

        return self.__class__(members=[member.replace_all_box(replacement) for member in self.members])

    def overestimate(self):
        return self.replace_all_box(Symbol.any_symbol().star()).simplify()

    def underestimate(self):
        return self.replace_all_box(Symbol.empty_lang()).simplify()

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

    def get_cost(self) -> int:
        if self._cost == -1:
            self._cost = self._calculate_cost()
        return self._cost

    def _calculate_cost(self) -> int:
        raise NotImplementedError("Should be implemented by child")


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

    def _compute_str(self):
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

    def _calculate_cost(self) -> int:
        return (len(self.members) - 1) * COST_MAP['∪'] + sum([member.get_cost() for member in self.members])

    def simplify(self):
        foo = self.members[0]
        for member in self.members[1:]:
            foo |= member.simplify()

        return foo

    @staticmethod
    def set_members(members):
        # should only be used in split for constructing arbitrary unions
        temp = Union(Symbol.empty_string(), Symbol.empty_string())
        temp.members = members
        return temp

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

    def _compute_str(self):
        # keep all non-ε
        self.members = [member for member in self.members if member.symbol != 'ε']

        return ''.join(str(member) for member in self.members)

    def _calculate_cost(self) -> int:
        return (len(self.members) - 1) * COST_MAP['⋅'] + sum([member.calculate_cost() for member in self.members])

    def simplify(self):
        foo = self.members[0]
        for member in self.members[1:]:
            foo += member.simplify()

        return foo

    @staticmethod
    def set_members(members):
        # should only be used in split for constructing arbitrary unions
        temp = Concatenation(Symbol.empty_string(), Symbol.empty_string())
        temp.members = members
        return temp

class Star(Pattern):
    def __init__(self, first: Pattern):
        super().__init__(members=[first])

    def _compute_str(self):
        if isinstance(self.members[0], Symbol) or str(self.members[0])[-1] == ')':
            return f"{self.members[0]}*"
        return f"({self.members[0]})*"

    def _calculate_cost(self) -> int:
        return COST_MAP['*'] + self.members[0].get_cost()

    def simplify(self):
        if isinstance(self.members[0], Star):
            return self.members[0].simplify()
        return self.members[0].simplify().star()


class Symbol(Pattern):
    def __init__(self, symbol: str):
        super().__init__(symbol=symbol)

    def _compute_str(self):
        return self.symbol

    def _calculate_cost(self) -> int:
        return 1

    def simplify(self):
        return self

    @staticmethod
    def empty_string():
        return Symbol('ε')

    @staticmethod
    def empty_lang():
        return Symbol('∅')

    @staticmethod
    def any_symbol():
        return Symbol('.')

class Box(Pattern):
    def __init__(self):
        super().__init__(symbol='☐')
        self.future = None

    def _compute_str(self):
        return self.symbol

    def _calculate_cost(self) -> int:
        return COST_MAP['☐']

    def simplify(self):
        if self.future:
            return self.future.simplify()
        return self

    def set_future(self, future: Pattern):
        self.future = future
