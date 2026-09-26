"""The DOGCAT word-change problem."""

import gzip
import string
from pathlib import Path

import search


dict_file = Path(__file__).with_name("words34.txt.gz")
dictionary = {}

with gzip.open(dict_file, "rt") as word_file:
    for line in word_file:
        word, rarity = line.strip().split("\t")
        dictionary[word] = float(rarity)

letter_values = {}
for letters, value in [
    ("aeioulnstr", 1),
    ("dg", 2),
    ("bcmp", 3),
    ("fhvwy", 4),
    ("k", 5),
    ("jx", 6),
    ("qz", 10),
]:
    for letter in letters:
        letter_values[letter] = value


class DC(search.Problem):
    def __init__(self, initial="dog", goal="cat", cost="steps"):
        if not isinstance(initial, str) or not isinstance(goal, str):
            raise ValueError("Words must be lowercase strings")
        if len(initial) not in (3, 4) or len(goal) != len(initial):
            raise ValueError("Words must have the same length of 3 or 4")
        if initial not in dictionary or goal not in dictionary:
            raise ValueError("Both words must be in the dictionary")
        if cost not in ("steps", "scrabble", "frequency"):
            raise ValueError("Unknown cost measure")

        super().__init__(initial, goal)
        self.cost = cost

    def actions(self, state):
        moves = []
        for position in range(len(state)):
            for letter in string.ascii_lowercase:
                if letter != state[position]:
                    next_word = state[:position] + letter + state[position + 1:]
                    if next_word in dictionary:
                        moves.append((position, letter))
        return moves

    def result(self, state, action):
        position, letter = action
        return state[:position] + letter + state[position + 1:]

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        if self.cost == "steps":
            return c + 1
        if self.cost == "scrabble":
            return c + letter_values[action[1]]
        return c + 1 + dictionary[state2]

    def h(self, node):
        state = node.state
        if self.cost == "scrabble":
            estimate = 0
            for position in range(len(state)):
                if state[position] != self.goal[position]:
                    estimate += letter_values[self.goal[position]]
            return estimate

        differences = 0
        for current, target in zip(state, self.goal):
            if current != target:
                differences += 1

        if self.cost == "frequency" and differences > 0:
            return differences + dictionary[self.goal]
        return differences

    def __repr__(self):
        return f"dc({self.initial},{self.goal},{self.cost})"
