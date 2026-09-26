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

letters = 'abcdefghijklmnopqrstuvwxyz'

scrabble = {}
for group, value in [('aeioulnstr', 1), ('dg', 2), ('bcmp', 3),
                     ('fhvwy', 4), ('k', 5), ('jx', 6), ('qz', 10)]:
    for ch in group:
        scrabble[ch] = value

min_rarity = {3: min(r for w, r in dictionary.items() if len(w) == 3),
              4: min(r for w, r in dictionary.items() if len(w) == 4)}

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
        # set instance attributes ...
        self.initial = initial
        self.goal = goal
        self.cost = cost
        # make sure arguments are legal, raising an error if any are bad.
        for w in (initial, goal):
            if not isinstance(w, str) or w not in dictionary or len(w) not in (3, 4) or not w.isalpha() or not w.islower():
                raise ValueError(f"bad word: {w!r}")
        if len(initial) != len(goal):
            raise ValueError("words must be the same length")
        if cost not in ('steps', 'scrabble', 'frequency'):
            raise ValueError(f"bad cost: {cost!r}")

    def actions(self, state):
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """
        acts = []
        for i in range(len(state)):
            for ch in letters:
                if ch != state[i] and state[:i] + ch + state[i+1:] in dictionary:
                    acts.append((i, ch))
        return acts

    def result(self, state, action):
        """ takes a state and an action and returns a new state """
        i, ch = action
        return state[:i] + ch + state[i+1:]

    def goal_test(self, state):
        """ returns True iff state is a goal state for this problem instance """
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """
        if self.cost == 'steps':
            return c + 1
        if self.cost == 'scrabble':
            return c + scrabble[action[1]]
        return c + 1 + dictionary[state2]          # frequency

    def __repr__(self):
        """" return a suitable string to represent this problem instance """
        return f"dc({self.initial},{self.goal},{self.cost})"

    def h(self, node):
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        wrong = [i for i in range(len(node.state)) if node.state[i] != self.goal[i]]
        if not wrong:
            return 0
        if self.cost == 'steps':
            return len(wrong)
        if self.cost == 'scrabble':
            return sum(scrabble[self.goal[i]] for i in wrong)
        return (len(wrong) - 1) * (1 + min_rarity[len(self.goal)]) + 1 + dictionary[self.goal]
