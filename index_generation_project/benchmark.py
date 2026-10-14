"""
Performance benchmark for the Index Generation project.

Measures:
1. Construction time
2. Search time using 100,000 random words
3. Printing time

Data sets:
1,000 / 5,000 / 10,000 / 50,000 / 100,000 / 500,000
distinct words.

Run:
    python benchmark.py

Results:
    benchmark_results.csv
    graphs/construction_time.png
    graphs/search_time.png
    graphs/printing_time.png
"""

import csv
import random
import time
from pathlib import Path

import matplotlib.pyplot as plt

from index_generator import (
    Trie,
    BST,
    DictionaryIndex,
    build_index,
    write_index,
    extract_words,
)

DATA_DIR = Path("data")
GRAPH_DIR = Path("graphs")
GRAPH_DIR.mkdir(exist_ok=True)

DISTINCT_COUNTS = [1000, 5000, 10000, 50000, 100000, 500000]

SEARCH_COUNT = 100_000
RANDOM_SEED = 12345


def create_index(kind):
    if kind == "Trie":
        return Trie()
    if kind == "BST":
        return BST()
    if kind == "Dictionary":
        return DictionaryIndex()

    raise ValueError(kind)


def get_all_words(filename):
    """
    Read words once for the search experiment.
    This reading is NOT included in construction timing.
    """
    words = []

    with open(filename, "r", encoding="ascii", errors="ignore") as file:
        for line in file:
            words.extend(extract_words(line))

    return words


def construction_time(filename, kind):
    index = create_index(kind)

    start = time.perf_counter()
    build_index(filename, index)
    end = time.perf_counter()

    return index, end - start


def search_time(index, words):
    rng = random.Random(RANDOM_SEED)

    # Randomly choose 100,000 words from the input.
    search_words = [
        words[rng.randrange(len(words))]
        for _ in range(SEARCH_COUNT)
    ]

    start = time.perf_counter()

    found = 0

    for word in search_words:
        if index.search(word) is not None:
            found += 1

    end = time.perf_counter()

    # Keep the result so Python does not treat the search as unused work.
    if found == -1:
        print("Impossible")

    return end - start


def printing_time(index, output_filename):
    start = time.perf_counter()

    write_index(output_filename, index)

    end = time.perf_counter()

    return end - start


def save_csv(results):
    filename = "benchmark_results.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "distinct_words",
            "implementation",
            "construction_seconds",
            "search_seconds",
            "printing_seconds",
        ])

        for row in results:
            writer.writerow(row)

    print("Saved:", filename)


def plot_metric(results, metric, title, filename):
    implementations = ["Trie", "BST", "Dictionary"]

    plt.figure(figsize=(10, 6))

    for implementation in implementations:
        x = []
        y = []

        for row in results:
            if row[1] == implementation:
                x.append(row[0])
                y.append(row[metric])

        plt.plot(
            x,
            y,
            marker="o",
            label=implementation,
        )

    plt.xlabel("Number of distinct words")
    plt.ylabel("Time (seconds)")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    output = GRAPH_DIR / filename
    plt.savefig(output, dpi=200)
    plt.close()

    print("Saved:", output)


def main():
    results = []

    for distinct_count in DISTINCT_COUNTS:
        input_file = DATA_DIR / f"input_{distinct_count}.txt"

        if not input_file.exists():
            print("Missing:", input_file)
            print("Run: python generate_test_files.py")
            return

        print("=" * 70)
        print("DATA SET:", distinct_count, "distinct words")
        print("=" * 70)

        # Read words once for random search selection.
        print("Reading search words...")
        words = get_all_words(input_file)

        for kind in ["Trie", "BST", "Dictionary"]:
            print()
            print("Testing:", kind)

            # ------------------------------------------------
            # 1. Construction time
            # ------------------------------------------------
            print("  Measuring construction...")
            index, construction = construction_time(
                input_file,
                kind,
            )

            # ------------------------------------------------
            # 2. Search time
            # ------------------------------------------------
            print("  Measuring 100,000 searches...")
            search = search_time(index, words)

            # ------------------------------------------------
            # 3. Printing time
            # ------------------------------------------------
            output_file = (
                Path("data")
                / f"output_{distinct_count}_{kind}.txt"
            )

            print("  Measuring printing...")
            printing = printing_time(
                index,
                output_file,
            )

            results.append([
                distinct_count,
                kind,
                construction,
                search,
                printing,
            ])

            print(
                f"  Construction : {construction:.6f} s"
            )
            print(
                f"  Search       : {search:.6f} s"
            )
            print(
                f"  Printing     : {printing:.6f} s"
            )

    save_csv(results)

    print()
    print("Creating graphs...")

    plot_metric(
        results,
        2,
        "Construction Time Comparison",
        "construction_time.png",
    )

    plot_metric(
        results,
        3,
        "Search Time Comparison - 100,000 Searches",
        "search_time.png",
    )

    plot_metric(
        results,
        4,
        "Printing Time Comparison",
        "printing_time.png",
    )

    print()
    print("Benchmark completed successfully.")


if __name__ == "__main__":
    main()
