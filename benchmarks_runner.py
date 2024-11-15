from search import GenerateRegex


def open_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content


import itertools


def replace_x_with_permutations(line):
    count_x = line.count('X')
    permutations = itertools.product('01', repeat=count_x)
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
    p = []
    n = []
    currently_positive = True
    for line in lines[1:]:
        if line == "++":
            currently_positive = True
        elif line == "--":
            currently_positive = False
        elif currently_positive:
            p.append(line)
        else:
            for perm in replace_x_with_permutations(line):
                n.append(perm)
    return name, p, n

def run_benchmark(f):
    name, p, n = read_benchmark(open_file(f'benchmarks/{f}'))
    solution = GenerateRegex(p, n)
    print(f"{f}: {name}")
    result = solution.search_algorithm()
    if result is None:
        print("No solution found")
    else:
        print(result)
        print(result.get_content())

def main():
    # run_benchmark('no02_end_with_01')

    import os
    files = os.listdir('benchmarks')
    files.sort()
    for file in files:
        run_benchmark(file)

if __name__ == '__main__':
    main()