"""
Index Generation Project
Chanakya University - Laboratory Examination 2

Usage:
    python index_generator.py input.txt output.txt trie
    python index_generator.py input.txt output.txt bst
    python index_generator.py input.txt output.txt dict

The assignment requires two command-line file arguments. The optional
third argument selects the implementation. If omitted, Trie is used.
"""

import sys


# ============================================================
# LINKED-LIST QUEUE OF LINE NUMBERS
# ============================================================

class LineNode:
    def __init__(self, line_number):
        self.line_number = line_number
        self.next = None


class LineQueue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, line_number):
        new_node = LineNode(line_number)

        if self.front is None:
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    def get_lines(self):
        result = []
        current = self.front

        while current is not None:
            result.append(current.line_number)
            current = current.next

        return result


# ============================================================
# TRIE
# ============================================================

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False
        self.lines = LineQueue()


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, line_number):
        current = self.root

        for ch in word:
            if ch not in current.children:
                current.children[ch] = TrieNode()

            current = current.children[ch]

        current.is_word = True
        current.lines.enqueue(line_number)

    def search(self, word):
        current = self.root

        for ch in word:
            if ch not in current.children:
                return None

            current = current.children[ch]

        if current.is_word:
            return current.lines

        return None

    def get_words(self):
        result = []

        def traverse(node, current_word):
            if node.is_word:
                result.append((current_word, node.lines.get_lines()))

            # Sorting children gives ASCII/lexicographic order.
            for ch in sorted(node.children.keys()):
                traverse(node.children[ch], current_word + ch)

        traverse(self.root, "")
        return result


# ============================================================
# BINARY SEARCH TREE
# ============================================================

class BSTNode:
    def __init__(self, word, line_number):
        self.word = word
        self.lines = LineQueue()
        self.lines.enqueue(line_number)
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, word, line_number):
        self.root = self._insert(self.root, word, line_number)

    def _insert(self, node, word, line_number):
        if node is None:
            return BSTNode(word, line_number)

        if word < node.word:
            node.left = self._insert(node.left, word, line_number)
        elif word > node.word:
            node.right = self._insert(node.right, word, line_number)
        else:
            # Repeated word: store another occurrence line number.
            node.lines.enqueue(line_number)

        return node

    def search(self, word):
        current = self.root

        while current is not None:
            if word == current.word:
                return current.lines
            elif word < current.word:
                current = current.left
            else:
                current = current.right

        return None

    def get_words(self):
        result = []

        def inorder(node):
            if node is None:
                return

            inorder(node.left)
            result.append((node.word, node.lines.get_lines()))
            inorder(node.right)

        # In-order traversal produces sorted order.
        inorder(self.root)
        return result


# ============================================================
# PYTHON DICTIONARY
# ============================================================

class DictionaryIndex:
    def __init__(self):
        self.index = {}

    def insert(self, word, line_number):
        if word not in self.index:
            self.index[word] = LineQueue()

        self.index[word].enqueue(line_number)

    def search(self, word):
        return self.index.get(word)

    def get_words(self):
        result = []

        for word in sorted(self.index.keys()):
            result.append((word, self.index[word].get_lines()))

        return result


# ============================================================
# COMMON FILE PROCESSING
# ============================================================

SEPARATORS = " \t\n\r.,:;"


def extract_words(line):
    """
    Replace only the separators specified in the question.
    Other printable ASCII characters remain part of a word.
    """
    for separator in SEPARATORS:
        line = line.replace(separator, " ")

    return line.split()


def build_index(filename, index):
    with open(filename, "r", encoding="ascii", errors="ignore") as file:
        line_number = 0

        for line in file:
            line_number += 1

            for word in extract_words(line):
                index.insert(word, line_number)


def write_index(filename, index):
    with open(filename, "w", encoding="ascii", errors="ignore") as file:
        for word, lines in index.get_words():
            file.write(word + " : ")
            file.write(" ".join(map(str, lines)))
            file.write("\n")


def create_index(kind):
    if kind == "trie":
        return Trie()

    if kind == "bst":
        return BST()

    if kind == "dict":
        return DictionaryIndex()

    raise ValueError("Implementation must be trie, bst, or dict")


def main():
    if len(sys.argv) not in (3, 4):
        print("Usage:")
        print("  python index_generator.py input.txt output.txt")
        print("  python index_generator.py input.txt output.txt trie")
        print("  python index_generator.py input.txt output.txt bst")
        print("  python index_generator.py input.txt output.txt dict")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    kind = sys.argv[3].lower() if len(sys.argv) == 4 else "trie"

    try:
        index = create_index(kind)
        build_index(input_file, index)
        write_index(output_file, index)
        print("Index generated successfully using:", kind)
        print("Output:", output_file)
    except FileNotFoundError:
        print("Input file not found:", input_file)
    except Exception as error:
        print("Error:", error)


if __name__ == "__main__":
    main()
