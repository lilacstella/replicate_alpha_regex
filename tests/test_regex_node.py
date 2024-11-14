import pytest
from regex_node import RegexNode

@pytest.fixture
def single_node():
    # 0
    return RegexNode('0')

@pytest.fixture
def concat_node():
    #  ⋅
    # a b
    return RegexNode('⋅', RegexNode('0'), RegexNode('1'))

@pytest.fixture
def union_node():
    #  ∪
    # a b
    return RegexNode('∪', RegexNode('0'), RegexNode('1'))

def test_single_node(single_node):
    assert single_node.value == '0'
    assert len(single_node.children) == 0

def test_concat_node(concat_node):
    assert concat_node.value == '⋅'
    assert len(concat_node.children) == 2
    assert concat_node.children[0].value == '0'
    assert concat_node.children[1].value == '1'

def test_union_node(union_node):
    assert union_node.value == '∪'
    assert len(union_node.children) == 2
    assert union_node.children[0].value == '0'
    assert union_node.children[1].value == '1'