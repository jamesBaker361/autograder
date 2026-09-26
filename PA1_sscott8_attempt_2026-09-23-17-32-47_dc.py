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
            raise ValueError("Initial and goal must be strings.")
        if not all('a' <= c <= 'z' for c in initial + goal):
            raise ValueError("Initial and goal must contain only lowercase letters.")
        if len(initial) not in (3, 4) or len(goal) not in (3, 4):
            raise ValueError("Initial and goal must be 3 or 4 letters long.")
        if len(initial) != len(goal):
            raise ValueError("Initial and goal must have the same length.")
        if initial not in dictionary or goal not in dictionary:
            raise ValueError("Initial and goal must exist in the dictionary.")
        if cost not in ('steps', 'scrabble', 'frequency'):
            raise ValueError("Invalid cost measure.")
        super().__init__(initial, goal)
        self.cost = cost

    def actions(self, state):
        """Return all legal one-letter replacement actions."""
        possible_actions = []
        for i in range(len(state)):
            for letter in 'abcdefghijklmnopqrstuvwxyz':
                if letter == state[i]:
                    continue
                new_word = state[:i] + letter + state[i+1:]
                if new_word in dictionary:
                    possible_actions.append((i, letter))
        return possible_actions

    def result(self, state, action):
        """Return the state produced by applying an action."""
        position, letter = action
        new_state = state[:position] + letter + state[position+1:]
        return new_state

    def goal_test(self, state):
        """Return True if the current state is the goal state."""
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cumulative cost of reaching state2."""
        if self.cost == 'steps':
            return c + 1
        elif self.cost == 'scrabble':
            scrabble_values = {
                'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1,
                'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
                'd': 2, 'g': 2,
                'b': 3, 'c': 3, 'm': 3, 'p': 3,
                'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
                'k': 5,
                'j': 6, 'x': 6,
                'q': 10, 'z': 10
            }
            position, letter = action
            return c + scrabble_values[letter]
        elif self.cost == 'frequency':
            return c + 1 + dictionary[state2]

    def __repr__(self):
        """Return a string representation of the problem instance."""
        return f"dc({self.initial},{self.goal},{self.cost})"

    def h(self, node):
        """Return an admissible estimate of the remaining cost."""
        state = node.state
        if self.cost == 'steps':
            return sum(
                state[i] != self.goal[i]
                for i in range(len(state))
            )
        elif self.cost == 'scrabble':
            scrabble_values = {
                'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1,
                'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
                'd': 2, 'g': 2,
                'b': 3, 'c': 3, 'm': 3, 'p': 3,
                'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
                'k': 5,
                'j': 6, 'x': 6,
                'q': 10, 'z': 10
            }
            return sum(
                scrabble_values[self.goal[i]]
                for i in range(len(state))
                if state[i] != self.goal[i]
            )
        elif self.cost == 'frequency':
            return sum(
                state[i] != self.goal[i]
                for i in range(len(state))
            )
