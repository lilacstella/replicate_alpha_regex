import pytest
from regex_node import RegexNode

def test_initializes_correctly():
    a = RegexNode("☐")
    assert a.value == "☐"
    for char in ["0", "1", "ε", "∅", ".", "∪", "⋅", "*"]:
        b = RegexNode(char)
        print(b.value)
        assert b.value == char
        assert b.children == []

def test_display_single_node():
    a = RegexNode("☐")
    assert a.display() == "☐\n"

def test_display_two_children():
    b = RegexNode("∪")
    b.children = [RegexNode("0"), RegexNode("1")]
    assert b.display() == "∪\n\t0\n\t1\n"

def test_display_single_child():
    c = RegexNode("*")
    c.children = [RegexNode("0")]
    assert c.display() == "*\n\t0\n"