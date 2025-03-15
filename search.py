import heapq
import re
import collections
import copy
import time
from regex_tree import RegexTree
from regex_node import RegexNode

# P = ["0", "01", "011", "000", "00"]
# N = ["1", "10", "11", "100", "101"]

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

    def is_solution(self, s: RegexTree):
        """
        This function checks if a given state is a solution to the problem.
        :param s: the regex state to check
        :return: whether the state is a solution or not
        """
        if "☐" in s.get_content():
            return False

        for p in self.P:
            if not re.fullmatch(s.get_content(), p):
                return False
        for n in self.N:
            if re.fullmatch(s.get_content(), n):
                return False

        return True

    def next_state(self, s: RegexTree):
        """
        This function generates the next states from a given state. This is the core of the search algorithm.
        It generates all possible states from the given state by filling in each hole with all possible values.
        :param s: regex state to generate next states from
        :return: potential future states to explore
        """
        if "☐" not in s.get_content():
            return []

        # next(s) = { s' | s -> s'}
        # if it makes it here this state already failed
        # apply all the implied operations upon all holes
        # and discard it after we extract all its states
        output = []
        # print(f"generating new states from \n{s.get_content()}")
        clone_root = copy.deepcopy(s.get_root())

        queue = collections.deque([clone_root])
        while queue:
            node = queue.popleft()
            if node.value == "☐":
                for replacement in ["0", "1", "ε", "∅", "."]:
                    # currently I have a reference to the original tree node with a hole
                    node.value = replacement
                    output.append(copy.deepcopy(clone_root))

                # alternating tree to add children
                node.value = "*"
                node.children = [RegexNode("☐")]
                output.append(copy.deepcopy(clone_root))
                node.children.append(RegexNode("☐"))
                for replacement in ["∪", "⋅"]:
                    node.value = replacement
                    output.append(copy.deepcopy(clone_root))
                node.value = "☐"
                node.children = []
            else:
                queue.extend(node.children)

        output = [RegexTree(root) for root in output]

        # kill dead states, match all positive, doesn't match any negative
        def matches_all_positive(state):
            # i should actually make an entire clone of the tree, then replace the nodes with .* and check if it matches
            return all(re.fullmatch(state.get_content().replace('☐', '(.*)'), p) for p in self.P)
        def matches_no_negative(state):
            # because here we need to do so in null alphabet and string
            # so we want to substitute on the tree level, simplify it, and then match the regex
            # i need to simplify, but not make a permanent change, only for the regex matching
            return not any(re.fullmatch(state.get_content().replace('☐', '(.*)'), n) for n in self.N)

        output = [state for state in output if matches_all_positive(state) and matches_no_negative(state)]

        # generate and narrow redundant states
        # print("------------------------")
        # for i in output:
        #     print(i.display())

        return output

    def search_algorithm(self):
        """
        This function is the main search algorithm for the problem. It uses a priority queue to explore the search space.
        Iteratively verifying whether a state is a solution or not,
        and generating the next states from a given state of it has more potential to explore.
        :return: 
        """
        start_time = time.time()
        w: list = [RegexTree()]  # Priority queue
        while w:
            if time.time() - start_time > 30:
                return None
            # Get the next element from the priority queue
            s: RegexTree = heapq.heappop(w)

            print(s)
            print(s.get_content())
            # it should fail the states with holes and let next_state fill them in
            if self.is_solution(s):
                return s
            for potential_state in self.next_state(s):
                heapq.heappush(w, potential_state)

        return None
