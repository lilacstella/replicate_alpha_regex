import heapq
import re
import collections
import copy
import time
from alpha_regex import alphabet, time_to_run
from alpha_regex.pattern import Pattern, Union, Concatenation, Star, Symbol, Box


class GenerateRegex:
    """
    This class represents a problem of generating a regex that matches all positive examples and none of the negative examples.
    It's attributes pertain to the constraints of the problem.
    """

    def __init__(self, p, n):
        """
        The constructor for the GenerateRegex class.
        :param p: positive examples as a list of strings
        :param n: negative examples as a list of strings
        """
        self.P = p
        self.N = n

    def is_solution(self, pattern: Pattern):
        """
        This function checks if a given state is a solution to the problem.
        :param pattern: the regex state to check
        :return: whether the state is a solution or not
        """
        # save some effort str-ifying the pattern
        for p in self.P:
            if not re.fullmatch(str(pattern), p):
                return False
        for n in self.N:
            if re.fullmatch(str(pattern), n):
                return False

        return True

    def matches_all_positive(self, state: Pattern):
        return all(re.fullmatch(str(state.overestimate()), p) for p in self.P)

    def matches_no_negative(self, state: Pattern):
        return not any(re.fullmatch(str(state.underestimate()), n) for n in self.N)

    def kill_dead_states(self, states: list[Pattern]):
        # kill dead states, match all positive, doesn't match any negative
        return [
            state
            for state in states
            if self.matches_all_positive(state) and self.matches_no_negative(state)
        ]

    def kill_redundant_states(self, states: list[Pattern]):
        def unroll(state):
            if isinstance(state, Star):
                return Concatenation.set_members([state.members[0], state.members[0], state])

            if isinstance(state, Symbol) or isinstance(state, Box):
                return state

            # Union or Concatenation
            return state.__class__.set_members([unroll(member) for member in state.members])

        def split(state) -> list[Pattern]:
            if isinstance(state, Box) or isinstance(state, Symbol) or isinstance(state, Star):
                return [state]

            if (isinstance(state, Concatenation) or isinstance(state, Union)) and len(state.members) == 1:
                return split(state.members[0])

            mid = len(state.members) // 2
            if isinstance(state, Union):
                return split(Union.set_members(state.members[:mid])) + split(Union.set_members(state.members[mid:]))

            # Concatenation
            out = []
            e_1 = Concatenation.set_members(state.members[:mid])
            e_2 = Concatenation.set_members(state.members[mid:])
            for e_1_prime in split(e_1):
                out.append(e_1_prime + e_2)
            for e_2_prime in split(e_2):
                out.append(e_1 + e_2_prime)

            return out

        return [state for state in states if all(self.matches_all_positive(expansion) for expansion in split(unroll(state)))]

    def next_state(self, src: Pattern):
        # next(s) = { s' | s -> s'}
        # if it makes it here this state already failed
        # apply all the implied operations upon all holes
        # and discard it after we extract all its states
        new_states = []

        queue = collections.deque([src])
        while queue:
            pattern = queue.popleft()
            if isinstance(pattern, Symbol):
                continue
            if isinstance(pattern, Box):
                for symbol in alphabet.union(set("ε∅.")):
                    pattern.set_future(Symbol(symbol))
                    new_states.append(copy.deepcopy(src))

                for operation in [
                    Box() + Box(),
                    Box() | Box(),
                    Box().star()
                ]:
                    pattern.set_future(operation)
                    new_states.append(copy.deepcopy(src))
            else:
                queue.extend(pattern.members)

        return self.kill_redundant_states(self.kill_dead_states(new_states))
        # return self.kill_dead_states(new_states)
        # return new_states

    def search_algorithm(self):
        """
        This function is the main search algorithm for the problem. It uses a priority queue to explore the search space.
        Iteratively verifying whether a state is a solution or not,
        and generating the next states from a given state of it has more potential to explore.
        :return: 
        """
        start_time = time.time()
        state_count = 0
        w: list = [Box()]  # Priority queue
        while w:
            if time.time() - start_time > time_to_run:
                return None, state_count
            # Get the next element from the priority queue
            s: Pattern = heapq.heappop(w)
            state_count += 1
            if not s.contains_box():
                s = s.simplify()
                if self.is_solution(s):
                    return s, state_count
                continue

            for potential_state in self.next_state(s):
                heapq.heappush(w, potential_state)

        return None, state_count
