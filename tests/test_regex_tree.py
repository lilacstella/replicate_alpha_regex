import pytest
from regex_tree import RegexTree
from regex_node import RegexNode

@pytest.fixture
def sample_tree():
    tree = RegexTree("∪")
    tree.root.children.append(RegexNode("a"))
    tree.root.children.append(RegexNode("b"))
    print(tree.display())
    return tree

def test_initializes_correctly(sample_tree):
    assert sample_tree.root.value == "∪"
    assert len(sample_tree.root.children) == 2

def test_deep_copy_creates_identical_tree(sample_tree):
    copied_tree = sample_tree.deep_copy()
    assert copied_tree.display() == sample_tree.display()

def test_interpret_returns_correct_string(sample_tree):
    tree = RegexTree("☐")
    assert tree.interpret() == "☐"
    tree.root.value = "a"
    assert tree.interpret() == "a"
    assert sample_tree.interpret() == "(a|b)"
    tree = sample_tree.deep_copy()
    tree.root.children[0].value = "⋅"
    tree.root.children[0].children = [RegexNode("0"), RegexNode("1")]
    assert tree.interpret() == "((01)|b)"

def test_calculate_cost_returns_correct_value(sample_tree):
    assert sample_tree.cost > 0
    tree = RegexTree("☐")
    assert tree.cost == 10
    tree = RegexTree("0")
    assert tree.cost < sample_tree.cost