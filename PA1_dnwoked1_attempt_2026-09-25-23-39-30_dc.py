""" starter file for pa1: dogcat """

import search       # AIMA module for search problems
import gzip         # read from a gzip'd file
import string

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
    
SCRABBLE_SCORES = {
    'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1, 'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
    'd': 2, 'g': 2,
    'b': 3, 'c': 3, 'm': 3, 'p': 3,
    'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
    'k': 5,
    'j': 6, 'x': 6,
    'q': 10, 'z': 10
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
        #TODO: complete this
        # set instance attributes ...
        valid_costs = ('steps', 'scrabble', 'frequency')
        if cost not in valid_costs:
            raise ValueError(f"Invalid cost measure")

        if not isinstance(initial, str) or not isinstance(goal, str):
            raise ValueError(f"Initial and goal must be strings")

        if initial != initial.lower() or goal != goal.lower():
            raise ValueError(f"Initial and goal must be strictly lowercase")

        if len(initial) not in (3,4) or len(goal) not in (3,4):
            raise ValueError(f"Initial and goal must be 3 or 4 characters in length")

        if len(initial) != len(goal):
            raise ValueError(f"Words must be equal length")

        if initial not in dictionary or goal not in dictionary:
            raise ValueError(f"Both words must be in dictionary")

        super().__init__(initial, goal)
        self.cost = cost

    def actions(self, state):
        legal_actions = []
        for pos in range(len(state)):
            current_char = state[pos]
            for char in string.ascii_lowercase:
                if char != current_char:
                    candidate_word = state[:pos] + char + state[pos + 1:]
                    if candidate_word in dictionary:
                        legal_actions.append((pos, char))
        return legal_actions

    def result(self, state, action):
        pos, char = action
        return state[:pos] + char + state[pos+1:]

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        if self.cost == 'steps':
            return c + 1
        elif self.cost == 'scrabble':
            pos, char = action
            return c + SCRABBLE_SCORES[char]
        elif self.cost == 'frequency':
            return c + 1.0 + dictionary[state2]
        else:
            raise ValueError(f"Unknown cost measure")

    def __repr__(self):
        return f"dc({self.initial},{self.goal},{self.cost})"

    def h(self, node):
        state = node.state if hasattr(node, 'state') else node
        
        mismatch_indices = [i for i in range(len(state)) if state[i] != self.goal[i]]
        mismatch_count = len(mismatch_indices)

        if self.cost == 'steps':
            return mismatch_count

        elif self.cost == 'scrabble':
            return sum(SCRABBLE_SCORES[self.goal[i]] for i in mismatch_indices)

        elif self.cost == 'frequency':
            return mismatch_count

        return 0