#Akanksha Madhu Kiran - submission
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

SCRABBLE_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4,
    'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3,
    'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8,
    'y': 4, 'z': 10,
}

VALID_COSTS = ('steps', 'scrabble', 'frequency')
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def rarity(word):
    """Negative log frequency; common words -> low, rare words -> high."""
    return dictionary[word]


def _min_rarity(length):
    """Smallest rarity() among dictionary words of the given length."""
    same_length_rarities = []
    for w in dictionary:
        if len(w) == length:
            same_length_rarities.append(dictionary[w])
    if same_length_rarities:
        return min(same_length_rarities)
    else:
        return 0.0

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
        #TODO: complete this - done
        self.valid = True
        try:
            assert isinstance(initial, str) and isinstance(goal, str), "initial and goal must be strings"
            assert initial == initial.lower() and goal == goal.lower(), "initial and goal must be lowercase"
            assert len(initial) in (3, 4), "words must be three or four letters long"
            assert len(initial) == len(goal), "initial and goal must be the same length"
            assert initial in dictionary and goal in dictionary, "initial and goal must both appear in the dictionary"
            assert cost in VALID_COSTS, "cost must be one of %s" % (VALID_COSTS,)
        except AssertionError:
            print("Invalid")
            return

        super().__init__(initial, goal)
        self.cost = cost

        if cost == 'frequency':
            self._min_rarity = _min_rarity(len(initial))
        else:
            None


    def actions(self, state):
        #TODO: complete this - done
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """
        acts = []
        for i in range(len(state)):
            for c in ALPHABET:
                if c == state[i]:
                    continue
                candidate = state[:i] + c + state[i + 1:]
                if candidate in dictionary:
                    acts.append((i, c))
        return acts


    def result(self, state, action):
        #TODO: complete this - done
        """ takes a state and an action and returns a new state """
        i, c = action
        return state[:i] + c + state[i + 1:]

    def goal_test(self, state):
        #TODO: complete this - done
        """ returns True iff state is a goal state for this problem instance """
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        #TODO: complete this - done
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """
        if self.cost == 'steps':
            return c + 1
        elif self.cost == 'scrabble':
            _, new_letter = action
            return c + SCRABBLE_VALUES[new_letter]
        elif self.cost == 'frequency':
            return c + 1 + rarity(state2)
        else:
            print("unknown cost measure: %r" % (self.cost,))
            return c

    def __repr__(self):
        #TODO: complete this - done
        """" return a suitable string to represent this problem instance """
        return "DC(initial=%r, goal=%r, cost=%r)" % (self.initial, self.goal, self.cost)

    def h(self, node):
        #TODO: complete this - done
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        state = node.state
        if state == self.goal:
            return 0

        diffs = []

        for i in range(len(state)):
            if state[i] != self.goal[i]:
                diffs.append(i)
        n_diff = len(diffs)

        if self.cost == 'steps':
            return n_diff
        elif self.cost == 'scrabble':
            return sum(SCRABBLE_VALUES[self.goal[i]] for i in diffs)
        elif self.cost == 'frequency':
            last_action_cost = 1 + rarity(self.goal)
            other_actions_cost = (n_diff - 1) * (1 + self._min_rarity)
            return other_actions_cost + last_action_cost
        else:
            print("unknown cost measure: %r" % (self.cost,))
            return
