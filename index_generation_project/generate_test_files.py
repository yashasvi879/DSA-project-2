"""
Generate six large test files for the Index Generation project.

The six files contain MORE THAN 1,000,000 total words and have
approximately:
    1,000
    5,000
    10,000
    50,000
    100,000
    500,000
distinct words.

Usage:
    python generate_test_files.py

The generated files are placed in the data/ directory.

WARNING:
The 500,000-distinct-word file can be large and may take time
and disk space to generate.
"""

from pathlib import Path
import random
import string

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

DISTINCT_COUNTS = [1000, 5000, 10000, 50000, 100000, 500000]

# At least 1,000,001 words in every file.
TOTAL_WORDS = 1_000_100

WORDS_PER_LINE = 20
RANDOM_SEED = 42


def make_word(number):
    """
    Create printable-ASCII words.
    Letters/digits are used here so the generated data is easy to inspect.
    """
    return "word" + str(number)


def generate_file(distinct_count):
    filename = DATA_DIR / f"input_{distinct_count}.txt"

    words = [make_word(i) for i in range(distinct_count)]

    rng = random.Random(RANDOM_SEED + distinct_count)

    print(f"Generating {filename} ...")
    print(f"Distinct words: {distinct_count}")
    print(f"Total words:    {TOTAL_WORDS}")

    with open(filename, "w", encoding="ascii") as file:
        remaining = TOTAL_WORDS

        while remaining > 0:
            count = min(WORDS_PER_LINE, remaining)

            line_words = [
                words[rng.randrange(distinct_count)]
                for _ in range(count)
            ]

            # Use several permitted separators.
            separator = rng.choice([" ", "  ", ".", ",", ":", ";"])
            line = separator.join(line_words)

            file.write(line + "\n")
            remaining -= count

    print("Finished:", filename)
    print()


def main():
    for count in DISTINCT_COUNTS:
        generate_file(count)


if __name__ == "__main__":
    main()
