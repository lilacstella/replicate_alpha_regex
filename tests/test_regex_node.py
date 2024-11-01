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

def test_display_nested_children():
    d = RegexNode("∪")
    d.children = [RegexNode("0"), RegexNode("∪")]
    d.children[1].children = [RegexNode("1"), RegexNode("⋅"), RegexNode("0")]
    d.children[1].children[1].children = [RegexNode("a"), RegexNode("b"), RegexNode("c")]
    print()
    print(d.display())
    assert d.display() == "∪\n\t0\n\t∪\n\t\t1\n\t\t⋅\n\t\t\ta\n\t\t\tb\n\t\t\tc\n\t\t0\n"
    d.children.reverse()
    print()
    print(d.display())
    assert d.display() == "∪\n\t∪\n\t\t1\n\t\t⋅\n\t\t\ta\n\t\t\tb\n\t\t\tc\n\t\t0\n\t0\n"