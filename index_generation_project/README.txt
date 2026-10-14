# Index Generation Project

## Files

- `index_generator.py` - Trie, BST and Dictionary implementations.
- `generate_test_files.py` - creates six large input files.
- `benchmark.py` - measures construction, search and printing time and creates Matplotlib graphs.
- `sample_input.txt` - small test file.
- `graphs/` - generated graphs.
- `data/` - generated large input/output files.

## Install Matplotlib

```text
python -m pip install matplotlib
```

## Test the main program

```text
python index_generator.py sample_input.txt output_trie.txt trie
python index_generator.py sample_input.txt output_bst.txt bst
python index_generator.py sample_input.txt output_dict.txt dict
```

The required two-argument form also works:

```text
python index_generator.py sample_input.txt output.txt
```

The default implementation is Trie.

## Generate the six large files

```text
python generate_test_files.py
```

This creates:

```text
data/input_1000.txt
data/input_5000.txt
data/input_10000.txt
data/input_50000.txt
data/input_100000.txt
data/input_500000.txt
```

Each contains more than 1,000,000 words.

## Run the benchmark

```text
python benchmark.py
```

It measures:

1. Construction time
2. Search time for 100,000 random words
3. Printing time

It creates:

```text
benchmark_results.csv
graphs/construction_time.png
graphs/search_time.png
graphs/printing_time.png
```

## Important

The generated 500,000-distinct-word file is large. Make sure your computer has enough free disk space.

The benchmark timings are machine-dependent. Do not write fixed timing values in the report before actually running the benchmark on your computer.
