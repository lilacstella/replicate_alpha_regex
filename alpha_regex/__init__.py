alphabet = set('ab')

# a, b, ☐, ε, ∅, ., ∪, ⋅, *
COST_MAP = {
    "☐": 100,
    "∪": 30,
    "⋅": 5,
    "*": 20,
    "a": 20,
}

benchmark_to_run = 'all'
# seconds
time_to_run = 60

