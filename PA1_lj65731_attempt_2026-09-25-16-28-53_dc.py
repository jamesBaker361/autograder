""" starter file for pa1: dogcat """

import search       # AIMA module for search problems
import gzip         # read from a gzip'd file
import string
import math

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
        # set instance attributes
        self.initial = initial.lower()
        self.goal = goal.lower()
        self.cost = cost

        # validate words
        if len(self.initial) != len(self.goal):
            raise ValueError('Initial and goal words must have same length')
        if self.initial not in dictionary:
            raise ValueError(f'Initial word "{self.initial}" not in dictionary')
        if self.goal not in dictionary:
            raise ValueError(f'Goal word "{self.goal}" not in dictionary')

    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        state = state.lower()
        actions = []
        letters = string.ascii_lowercase
        for i in range(len(state)):
            for ch in letters:
                if ch == state[i]:
                    continue
                candidate = state[:i] + ch + state[i+1:]
                if candidate in dictionary:
                    actions.append(candidate)
        return actions

    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        # In our implementation an action is simply the resulting word
        return action

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        #TODO: complete this
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """
        # state2 is the resulting word (one-letter different from state1)
        if self.cost == 'steps':
            return c + 1
        elif self.cost == 'scrabble':
            # cost is the scrabble value of the changed letter(s) in state2
            # define standard Scrabble scores
            scores = {
                **dict.fromkeys(list('aeioulnstr'), 1),
                **dict.fromkeys(list('dg'), 2),
                **dict.fromkeys(list('bcmp'), 3),
                **dict.fromkeys(list('fhvwy'), 4),
                    'k': 5,
                    **dict.fromkeys(list('jx'), 6),
                    **dict.fromkeys(list('qz'), 10)
            }
            # sum scores for differing letters (should be one)
            diff_score = 0
            for a, b in zip(state1, state2):
                if a != b:
                    diff_score += scores.get(b, 0)
            return c + diff_score
        elif self.cost == 'frequency':
            # cost is 1 + rarity(state2) according to the assignment PDF
            # dictionary stores a nonnegative rarity value per word
            rarity = dictionary.get(state2, 0.0)
            return c + 1 + rarity
        else:
            raise ValueError('Unknown cost metric: ' + str(self.cost))

    def __repr__(self):
        return f"DC({self.initial}->{self.goal},cost={self.cost})"

    def h(self, node):
        state = node.state
        # steps: number of differing letters (Hamming distance)
        if self.cost == 'steps':
            return sum(1 for a, b in zip(state, self.goal) if a != b)
        elif self.cost == 'scrabble':
            # admissible: sum of scrabble scores of goal letters at differing positions
            scores = {
                **dict.fromkeys(list('aeioulnstr'), 1),
                **dict.fromkeys(list('dg'), 2),
                **dict.fromkeys(list('bcmp'), 3),
                **dict.fromkeys(list('fhvwy'), 4),
                'k': 5,
                **dict.fromkeys(list('jx'), 8),
                **dict.fromkeys(list('qz'), 10)
            }
            return sum(scores.get(b, 0) for a, b in zip(state, self.goal) if a != b)
        elif self.cost == 'frequency':
            # admissible heuristic for frequency: each differing letter requires at least
            # one action, and each action costs at least 1 (plus a nonnegative rarity),
            # so lower bound is number of differing positions * 1
            mismatches = sum(1 for a, b in zip(state, self.goal) if a != b)
            return mismatches * 1
        else:
            return 0
