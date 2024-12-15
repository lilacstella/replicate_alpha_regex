from search import GenerateRegex
import time


def open_file(file_path):
    """
    Open a file and return its content
    :param file_path: The filepath to be opened
    :return: The content of the file as a str
    """
    with open(file_path, 'r') as file:
        content = file.read()
    return content


import itertools


def replace_x_with_permutations(line):
    """
    Replace all X's in a line with all possible permutations of 0 and 1, to expand the examples specified with wildcards
    :param line: a line from the benchmarks
    :return: a list of all possible permutations of the line
    """
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
    """
    Read the content of a benchmark file and return the name, positive and negative examples
    :param content: Benchmark file contents as a string in the format of the problem
    :return: Python variables of the inputs to a regex generation problem
    """
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
    """
    Execute the search algorithm on a benchmark file and write the results to a file
    :param f: The filename of the baenchmark file
    :return: None
    """
    name, p, n = read_benchmark(open_file(f'benchmarks/{f}'))
    solution = GenerateRegex(p, n)
    with open('results.txt', 'a') as file:
        file.write(f"{f}: {name}\n")
        now = time.time()
        result = solution.search_algorithm()
        if result is None:
            file.write("No solution found\n")
        else:
            file.write(f'{result}\n')
            file.write(f'{result.get_content()}\n')
        file.write(f'Time: {time.time() - now}\n\n')

def run_all_benchmarks():
    """
    Run all benchmarks in the benchmarks folder
    :return: None
    """
    import os
    files = os.listdir('benchmarks')
    files.sort()
    for file in files:
        run_benchmark(file)

def main():
    reset = True
    if reset:
        with open('results.txt', 'w') as file:
            pass

    # run_benchmark('no01_start_with_0')
    run_all_benchmarks()

if __name__ == '__main__':
    main()