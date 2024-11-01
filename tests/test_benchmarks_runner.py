import pytest
import textwrap

import benchmarks_runner

@pytest.fixture()
def a():
    return """
w starts with 0
++
0
0X
0XX
--
1
1X
1XX
           """.strip()

@pytest.fixture()
def b():
    return """
whatever
++
a
b
c
--
1
2
3
           """.strip()

@pytest.fixture()
def c():
    return """
w does not contain 100 as a substring
++
X
XX
0XX
X1X
XX1
X101
0X01X
XX1X1X1
--
100
X100
100X
X100X
           """.strip()

def test_read_benchmark(a, b, c):
    name, P, N = benchmarks_runner.read_benchmark(a)
    assert name == "w starts with 0"
    assert P == ["0", "0X", "0XX"]
    assert N == ["1", "1X", "1XX"]
    name, P, N = benchmarks_runner.read_benchmark(b)
    assert name == "whatever"
    assert P == ["a", "b", "c"]
    assert N == ["1", "2", "3"]
    name, P, N = benchmarks_runner.read_benchmark(c)
    assert name == "w does not contain 100 as a substring"
    assert P == ["X", "XX", "0XX", "X1X", "XX1", "X101", "0X01X", "XX1X1X1"]
    assert N == ["100", "X100", "100X", "X100X"]

def test_open_file():
    name, P, N = benchmarks_runner.read_benchmark(benchmarks_runner.open_file("benchmarks/no1_start_with_0"))
    assert name == "w starts with 0"
    assert P == ["0", "0X", "0XX"]
    assert N == ["1", "1X", "1XX"]
    name, P, N = benchmarks_runner.read_benchmark(benchmarks_runner.open_file("benchmarks/no19_not_contain_substring_100"))
    assert name == "w does not contain 100 as a substring"
    assert P == ["X", "XX", "0XX", "X1X", "XX1", "X101", "0X01X", "XX1X1X1"]
    assert N == ["100", "X100", "100X", "X100X"]