alphabet = set('ab')

# a, b, ☐, ε, ∅, ., ∪, ⋅, *
COST_MAP = {
    "☐": 10,
    "∪": 6,
    "⋅": 5,
    "*": 5,
}

benchmark_to_run = 'all'
# seconds
time_to_run = 60
