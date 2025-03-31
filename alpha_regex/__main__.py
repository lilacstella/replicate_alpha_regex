from alpha_regex import COST_MAP, benchmark_to_run, time_to_run
from alpha_regex.benchmarks_runner import run_benchmark, run_all_benchmarks

def main():
    reset = True
    if reset:
        with open('results.txt', 'w') as f:
            f.write(f'{COST_MAP=}\n')
            f.write(f'{time_to_run=} seconds\n')
            f.write(f'{benchmark_to_run=}\n\n\n')

    if benchmark_to_run == 'all':
        run_all_benchmarks()
    else:
        run_benchmark(benchmark_to_run)

if __name__ == '__main__':
    main()
