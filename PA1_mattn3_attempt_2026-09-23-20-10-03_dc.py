""" starter file for pa1: dogcat """

import search       # AIMA module for search problems
import gzip         # read from a gzip'd file
from pathlib import Path

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
for line in gzip.open(Path(__file__).with_name(dict_file), 'rt'):
    word, n = line.strip().split('\t')
    n = float(n)
    dictionary[word] = n

scrabble_values = {
    "a": 1, "b": 3, "c": 3, "d": 2, "e": 1, "f": 4,
    "g": 2, "h": 4, "i": 1, "j": 6, "k": 5, "l": 1,
    "m": 3, "n": 1, "o": 1, "p": 3, "q": 10, "r": 1,
    "s": 1, "t": 1, "u": 1, "v": 4, "w": 4, "x": 6,
    "y": 4, "z": 10,
}

class DC(search.Problem):
    """DC is a subclass of the AIMA search files's Problem class. Its init
       method takes three arguments: the initial word, goal word, and cost method.
       A state is represented as a lowercase string of three or four
       ascii characters.  Both the initial and goal states must be
       words of the same length and they must be in the dict
       dictionary. The cost argument specifies how to measure the
       cost of an action and can be 'steps', 'scrabble' or 'frequency'
       """

    def __init__(self, initial='dog', goal='cat', cost='steps'):
        if not isinstance(initial, str) or not isinstance(goal, str):
            raise ValueError("Initial and goal states must be strings")
        if initial != initial.lower() or goal != goal.lower():
            raise ValueError("Initial and goal states must be lowercase")
        if len(initial) not in (3, 4) or len(goal) not in (3, 4):
            raise ValueError("Initial and goal states must have three or four letters")
        if len(initial) != len(goal):
            raise ValueError("Initial and goal states must have the same length")
        if initial not in dictionary or goal not in dictionary:
            raise ValueError("Initial and goal states must be in the dictionary")
        if cost not in ("steps", "scrabble", "frequency"):
            raise ValueError("Cost must be steps, scrabble, or frequency")
        super().__init__(initial, goal)
        self.cost = cost

    def actions(self, state):
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        actions = []
        for position in range(len(state)):
            for character in "abcdefghijklmnopqrstuvwxyz":
                if character != state[position]:
                    candidate = state[:position] + character + state[position + 1:]
                    if candidate in dictionary:
                        actions.append((position, character))
        return actions

    def result(self, state, action):
        """ takes a state and an action and returns a new state """
        position, character = action
        return state[:position] + character + state[position + 1:]

    def goal_test(self, state):
        """ returns True iff state is a goal state for this problem instance """
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """
        if self.cost == "steps":
            return c + 1
        if self.cost == "scrabble":
            return c + scrabble_values[action[1]]
        return c + 1 + dictionary[state2]

    def __repr__(self):
        """ return a suitable string to represent this problem instance """
        return f"dc({self.initial},{self.goal},{self.cost})"

    def h(self, node):
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        mismatches = [
            position
            for position, (current, target) in enumerate(zip(node.state, self.goal))
            if current != target
        ]
        if self.cost == "steps":
            return len(mismatches)
        if self.cost == "scrabble":
            return sum(scrabble_values[self.goal[position]] for position in mismatches)
        if not mismatches:
            return 0
        return len(mismatches) + dictionary[self.goal]
