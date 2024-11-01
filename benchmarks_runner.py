import os
import search
from search import GenerateRegex


def open_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content


import itertools


def replace_x_with_permutations(line):
    count_X = line.count('X')
    permutations = itertools.product('01', repeat=count_X)
    results = []

    for perm in permutations:
        new_line = list(line)
        perm_index = 0
        for i, char in enumerate(new_line):
            if char == 'X':
                new_line[i] = perm[perm_index]
                perm_index += 1
        results.append(''.join(new_line))

    return results

def read_benchmark(content):
    lines = content.splitlines()
    name = lines[0]
    P = []
    N = []
    currently_positive = True
    for line in lines[1:]:
        if line == "++":
            currently_positive = True
        elif line == "--":
            currently_positive = False
        elif currently_positive:
            P.append(line)
        else:
            for perm in replace_x_with_permutations(line):
                N.append(perm)
    return name, P, N

def run_benchmark(f):
    name, P, N = read_benchmark(open_file(f'benchmarks/{f}'))
    solution = GenerateRegex(P, N)
    print(f"{f}: {name}")
    result = solution.search_algorithm()
    if result is None:
        print("No solution found")
    else:
        print(result.display())
        print(result.content)

def main():
    # run_benchmark('no2_end_with_01')

    for file in os.listdir('benchmarks'):
        run_benchmark(file)

if __name__ == '__main__':
    main()