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
    def __init__(self, p, n):
        self.P = p
        self.N = n

    def solution(self, s: RegexTree):
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

        # kill dead states
        matches_all_patterns = lambda state: all(re.fullmatch(state.get_content().replace('☐', '(.*)'), p) for p in self.P)
        output = [state for state in output if matches_all_patterns(state)]

        # generate and narrow redundant states
        # print("------------------------")
        # for i in output:
        #     print(i.display())

        return output

    def search_algorithm(self):
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
            if self.solution(s):
                return s
            for potential_state in self.next_state(s):
                heapq.heappush(w, potential_state)

        return None
