""" starter file for pa1: dogcat """

import search       # AIMA module for search problems
import gzip         # read from a gzip'd file
import os.path      # locate the dictionary next to this file
import string       # for string.ascii_lowercase

# file name for the dictionary, with one word per line.  Each line
# will have a word followed by a tab followed by a number, e.g.
#   and     0.07358445
#   for     0.18200336

dict_file = "words34.txt.gz"

# resolved against this file's own directory rather than the working
# directory, so dc can be imported or run from anywhere
dict_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), dict_file)

# dictionary is a dict to hold legal 3 and 4 letter words with their
# frequencies based on a sample of a large text corpus. The dict's
# keys are the words and its values are their frequencies

# load words into the dictionary dict
dictionary = {}
for line in gzip.open(dict_path, 'rt'):
    word, n = line.strip().split('\t')
    n = float(n)
    dictionary[word] = n

# the three cost metrics a DC problem instance can use
cost_metrics = ('steps', 'scrabble', 'frequency')

# cost of inserting each letter under the scrabble metric, using the
# values given in the assignment
scrabble_value = {letter: value
                  for value, letters in [(1, 'aeioulnstr'), (2, 'dg'), (3, 'bcmp'),
                                         (4, 'fhvwy'), (5, 'k'), (6, 'jx'), (10, 'qz')]
                  for letter in letters}


class DC(search.Problem):
    """DC is a subclass of the AIMA search files's Problem class. Its init
       method takes three arguments: the initial word, goal word, and cost method.
       A state is represented as a lowercase string of three or four
       ascii characters.  Both the initial and goal states must be
       words of the same length and they must be in the dict
       dictionary. The cost argument specifies how to measure the
       cost of an action and can be 'steps', 'scrabble' or 'frequency'

       An action is a (position, character) tuple, meaning replace the
       character at that position in the word with the given character.
       """

    def __init__(self, initial='dog', goal='cat', cost='steps'):
        # make sure arguments are legal, raising an error if any are bad
        for word, role in ((initial, 'initial'), (goal, 'goal')):
            if not isinstance(word, str):
                raise ValueError(f"{role} word must be a string: {word!r}")
            if word != word.lower():
                raise ValueError(f"{role} word must be lowercase: {word!r}")
            if len(word) not in (3, 4):
                raise ValueError(f"{role} word must have three or four letters: {word!r}")
            if word not in dictionary:
                raise ValueError(f"{role} word is not in the dictionary: {word!r}")
        if len(initial) != len(goal):
            raise ValueError(f"initial and goal words must be the same length: {initial!r}, {goal!r}")
        if cost not in cost_metrics:
            raise ValueError(f"cost must be one of {cost_metrics}: {cost!r}")
        # set instance attributes
        self.initial = initial
        self.goal = goal
        self.cost = cost

    def actions(self, state):
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        legal = []
        for i, old in enumerate(state):
            before, after = state[:i], state[i+1:]
            for char in string.ascii_lowercase:
                if char != old and before + char + after in dictionary:
                    legal.append((i, char))
        return legal

    def result(self, state, action):
        """ takes a state and an action and returns a new state """
        i, char = action
        return state[:i] + char + state[i+1:]

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
        elif self.cost == 'scrabble':
            # pay for the letter we just inserted
            return c + scrabble_value[action[1]]
        else:
            # frequency: entering a word costs 1 + its rarity
            return c + 1 + dictionary[state2]

    def __repr__(self):
        """" return a suitable string to represent this problem instance """
        return f"dc({self.initial},{self.goal},{self.cost})"

    def h(self, node):
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal.

        Every action fixes at most one position, so any path to the goal must
        include at least one action per position where the state and the goal
        differ.  Each heuristic below charges the cheapest price the metric
        allows for that unavoidable work, so none of them can overestimate.
        """
        state = node.state
        if state == self.goal:
            return 0
        if self.cost == 'steps':
            # every action costs 1, and at least one is needed per mismatch
            return mismatches(state, self.goal)
        elif self.cost == 'scrabble':
            # each mismatched position must receive the goal's letter at least
            # once, and inserting that letter always costs its scrabble value
            return sum(scrabble_value[g] for s, g in zip(state, self.goal) if s != g)
        else:
            # frequency: rarities are nonnegative, so each action costs at
            # least 1, and the last action must enter the goal word itself
            return (mismatches(state, self.goal) - 1) + (1 + dictionary[self.goal])


def mismatches(word1, word2):
    """ Returns the number of positions in which word1 and word2 differ """
    return sum(1 for c1, c2 in zip(word1, word2) if c1 != c2)
