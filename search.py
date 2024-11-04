import heapq
import re
import collections
from regex_tree import RegexTree, RegexNode

# P = ["0", "01", "011", "000", "00"]
# N = ["1", "10", "11", "100", "101"]

class GenerateRegex:
    def __init__(self, P, N):
        self.P = P
        self.N = N

    def solution(self, s: RegexTree):
        if "☐" in s.content:
            return False

        for p in self.P:
            if not re.fullmatch(s.content, p):
                # print(f"{s.content} did not match P")
                return False
        for n in self.N:
            if re.fullmatch(s.content, n):
                # print(f"{s.content} matched N")
                return False
        return True

    def next_state(self, s: RegexTree):
        if "☐" not in s.content:
            return []
        # next(s) = { s' | s -> s'}
        # if it makes it here this state already failed
        # apply all the implied operations upon all holes
        output = []
        # print(f"generating new states from \n{s.content}")
        original_tree = s.deep_copy()
        queue = collections.deque([original_tree.root])
        while queue:
            node = queue.popleft()
            if node.value == "☐":
                for replacement in ["0", "1", "ε", "∅", "."]:
                    # currently I have a reference to the original tree node with a hole
                    node.value = replacement
                    output.append(original_tree.deep_copy())
                node.value = "*"
                node.children = [RegexNode("☐")]
                output.append(original_tree.deep_copy())
                node.children.append(RegexNode("☐"))
                for replacement in ["∪", "⋅"]:
                    node.value = replacement
                    output.append(original_tree.deep_copy())
                node.value = "☐"
                node.children = []
            else:
                queue.extend(node.children)
            # print(queue)
        # print(output)
        # also kills all dead states and redundant states
        # for state in output:
            # print(state.content.replace("☐", ".*"))
            # re.fullmatch(state.content.replace("☐", ".*"), p) for p in self.P:

        matches_all_patterns = lambda state: all(re.fullmatch(state.content.replace("☐", ".*"), p) for p in self.P)
        output = [state for state in output if matches_all_patterns(state)]
        # return an iterable of states
        # print("------------------------")
        # for i in output:
        #     print(i.display())
        return output

    def search_algorithm(self):
        W: list = [RegexTree("☐")]  # Priority queue
        while W:
            # Get the next element from the priority queue
            s: RegexTree = heapq.heappop(W)

            # it should fail the states with holes and let next_state fill them in
            if self.solution(s):
                return s
            for potential_state in self.next_state(s):
                heapq.heappush(W, potential_state)

        return None
