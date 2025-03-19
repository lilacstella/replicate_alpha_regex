from alpha_regex.benchmarks_runner import run_benchmark, run_all_benchmarks

def main():
    reset = True
    if reset:
        with open('results.txt', 'w') as _:
            pass

    # run_benchmark('no01_start_with_a')
    run_all_benchmarks()

if __name__ == '__main__':
    main()
