""" starter file for pa1: dogcat """

import search       # AIMA module for search problems
import gzip         # read from a gzip'd file

# file name for the dictionary, with one word per line.  Each line
# will have a word followed by a tab followed by a number, e.g.
#   and     0.07358445
#   for     0.18200336

dict_file = "words34.txt.gz"

# dictionary is a dict to hold legal 3 and 4 letter words with their
# frequencies based on a sample of a large text corpus. The dict's
# keys are the words and its values are their frequencies

# load words into the dictionary dict
dictionary = {}
for line in gzip.open(dict_file, 'rt'):
    word, n = line.strip().split('\t')
    n = float(n)
    dictionary[word] = n

SCRABBLE = {letter: value for letters, value in (
    ("aeioulnstr", 1), ("dg", 2), ("bcmp", 3),
    ("fhvwy", 4), ("k", 5), ("jx", 6), ("qz", 10)
) for letter in letters}


class DC(search.Problem):
    """One-letter word transformations with three possible edge costs."""

    def __init__(self, initial='dog', goal='cat', cost='steps'):
        if (not isinstance(initial, str) or not isinstance(goal, str)
                or len(initial) not in (3, 4) or len(initial) != len(goal)
                or initial not in dictionary or goal not in dictionary
                or any(not ('a' <= ch <= 'z') for ch in initial + goal)):
            raise ValueError("initial and goal must be same-length lowercase dictionary words of length 3 or 4")
        if cost not in ('steps', 'scrabble', 'frequency'):
            raise ValueError("cost must be steps, scrabble, or frequency")
        super().__init__(initial, goal)
        self.cost = cost

    def actions(self, state):
        return [(i, letter) for i, old in enumerate(state)
                for letter in 'abcdefghijklmnopqrstuvwxyz' if letter != old
                and state[:i] + letter + state[i + 1:] in dictionary]

    def result(self, state, action):
        i, letter = action
        if (not isinstance(i, int) or i < 0 or i >= len(state)
                or letter not in 'abcdefghijklmnopqrstuvwxyz'
                or letter == state[i]):
            raise ValueError("invalid replacement action")
        target = state[:i] + letter + state[i + 1:]
        if target not in dictionary:
            raise ValueError("replacement does not produce a dictionary word")
        return target

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        if self.cost == 'steps':
            return c + 1
        if self.cost == 'scrabble':
            return c + SCRABBLE[action[1]]
        return c + 1 + dictionary[state2]

    def h(self, node):
        state = node.state
        mismatches = [i for i in range(len(state)) if state[i] != self.goal[i]]
        if self.cost == 'steps':
            return len(mismatches)
        if self.cost == 'scrabble':
            return sum(SCRABBLE[self.goal[i]] for i in mismatches)
        # Each mismatched position requires an action; every solution also
        # enters the goal exactly once, paying its rarity at that point.
        return len(mismatches) + (dictionary[self.goal] if mismatches else 0)

    def __repr__(self):
        return f"dc({self.initial},{self.goal},{self.cost})"

    __str__ = __repr__
