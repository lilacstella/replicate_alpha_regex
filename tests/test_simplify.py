from alpha_regex.pattern import Pattern, Union, Concatenation, Star, Symbol, Box

def test_simplify_concatenation():
    """
    Union
        Star
            Concatenation
                Star
                    Star
                        ☐ -> None
                .
        b
    """
    print()
    # pattern = Star(Box().star())
    # print(pattern.display_tree())
    # simplified_pattern = pattern.simplify()
    # print(simplified_pattern.display_tree())

    pattern = Star(Box().star()) + Symbol.any_symbol()
    print(pattern.display_tree())
    simplified_pattern = pattern.simplify()
    print(simplified_pattern.display_tree())

    # pattern = (Star(Box().star()) + Symbol.any_symbol()).star() | Symbol('b')
    # print(pattern.display_tree())
    # simplified_pattern = pattern.simplify()
    # print(simplified_pattern.display_tree())

def test_simplify_double_star():
    """
    (.*)*a
    """
    pattern = Star(Symbol.any_symbol().star())
    simplified_pattern = pattern.simplify()
    assert pattern.display_tree() != simplified_pattern.display_tree()

    pattern = Star(Symbol.any_symbol().star()) + Symbol("a")
    print(pattern.display_tree())
    simplified_pattern = pattern.simplify()
    assert pattern.display_tree() != simplified_pattern.display_tree()
    assert simplified_pattern.display_tree().replace(" ", "") == "Concatenation\nStar\n.\na\n"



def test_simplify_double_star_union():
    """
    ((a|b)*)*a
    """
    print()
    pattern = Star(Symbol("a") | Symbol("b")).star() + Symbol("a")
    print(pattern.display_tree())
    simplified_pattern = pattern.simplify()
    print(simplified_pattern.display_tree())
    assert pattern.display_tree() == "Concatenation\n  Star\n    Star\n      .\n  a\n"
    assert pattern.display_tree() != simplified_pattern.display_tree()
    assert simplified_pattern.display_tree() == "Concatenation\n  Star\n    .\n  a\n"

def test_simplify_union_null():
    """
    Union
        empty lang
        Star
            .
    """

    pattern = Union(Symbol.empty_lang(), Star(Symbol.any_symbol()))
    print(pattern.display_tree())
    simplified_pattern = pattern.simplify()
    print(simplified_pattern.display_tree())
    assert pattern.display_tree() != simplified_pattern.display_tree()

def test_simplify_concatenation_null():
    pattern = Concatenation(Symbol.empty_lang(), Star(Symbol.any_symbol()))
    print(pattern.display_tree())
    simplified_pattern = pattern.simplify()
    print(simplified_pattern.display_tree())
    assert pattern.display_tree() != simplified_pattern.display_tree()
    assert simplified_pattern.display_tree() == "∅"

def test_simplify_union_empty_string():
    """
    Union
        empty string
        Star
            .
    """

    pattern = Union(Symbol.empty_string(), Star(Symbol.any_symbol()))
    # print(pattern.display_tree())
    # print(pattern)
    simplified_pattern = pattern.simplify()
    # print(simplified_pattern.display_tree())
    # print(simplified_pattern)
    # assert pattern.display_tree() != simplified_pattern.display_tree()

    pattern = Symbol.any_symbol() + Union(Symbol.empty_string(), Union(Symbol.empty_string(), Symbol.any_symbol().star()))
    # print(pattern.display_tree())
    # print(pattern)
    simplified_pattern = pattern.simplify()
    # print(simplified_pattern.display_tree())
    # print(simplified_pattern)
    assert pattern.display_tree() != simplified_pattern.display_tree()
