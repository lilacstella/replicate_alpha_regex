# Replicating AlphaRegex

## AlphaRegex

[Synthesizing Regular Expressions from Examples
for Introductory Automata Assignments](https://cs.stanford.edu/~minalee/pdf/gpce2016-alpharegex.pdf)


[Source code from the original authors](https://github.com/kupl/AlphaRegexPublic)

## Running this project

This project consists of the solver, the `search.py` `GenerateRegex` class and a runner for examples. 
In `benchmark_runners.py`, you can find the main function, we configure the benchmarks to run in this function. 
The benchmarks are in the `benchmarks` folder. 

### Set up
Begin by making a python virtual environment and installing the dependencies.

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then, to execute the project: 
```shell
python -m alpha_regex
```

### Output
The output of the program will either display found solutions to the benchmarks or display that the solution was not found. This will be automatically written to a file
called `results.txt`. 

### Configuration

To specify a specific example, use `run_benchmark('name_of_benchmark_file')` in the main function, otherwise, to run all
examples, use `run_all_benchmarks()`.

To reset the `results.txt` file upon execution, leave the `reset` variable as true, otherwise set it to false. 

### Benchmark specification format
The benchmarks allow arbitrary names and needs to be specified in the following format:
```
description of the benchmark
++
01
001
0001
--
0
1X
110
```
The format starts with a description, then list positive examples after the `++` tag and negative examples after the `--` tag. The X allows for any character
