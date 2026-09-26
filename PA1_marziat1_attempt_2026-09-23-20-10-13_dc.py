""" starter file for pa1: dogcat """

import math          # for log2, used by the frequency cost metric
import search       # AIMA module for search problems
import gzip         # read from a gzip'd file
import string        # lowercase letters, used to generate candidate actions

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

# Standard Scrabble tile values, used by the 'scrabble' cost metric.
SCRABBLE_VALUES = {
    **{c: 1 for c in 'aeioulnstr'},
    **{c: 2 for c in 'dg'},
    **{c: 3 for c in 'bcmp'},
    **{c: 4 for c in 'fhvwy'},
    'k': 5,
    'j': 8, 'x': 8,
    'q': 10, 'z': 10,
}

# The raw numbers in the dictionary are corpus counts-per-million, not
# probabilities: common words like "and" have values well above 1, so
# -log2(raw_frequency) would be *negative* for them. Negative action costs
# break A* (there would be no well-defined cheapest path, since looping
# through cheap/negative-cost words could drive the cost to -infinity).
# Normalizing by the total turns the values into a proper probability
# distribution (they sum to 1), so every word's probability is < 1 and
# -log2(probability) is always positive.
TOTAL_FREQUENCY = sum(dictionary.values())


def frequency_cost(word):
    """ Cost of moving to `word` under the 'frequency' cost metric: rarer
    words (smaller frequency) cost more, and the cost is always positive. """
    probability = dictionary[word] / TOTAL_FREQUENCY
    return -math.log2(probability)


# The cheapest possible per-action cost for each cost metric. Used by h() to
# build an admissible (never-overestimating) heuristic: hamming_distance is a
# lower bound on the number of actions still needed, and multiplying it by
# the cheapest possible cost of a single action gives a lower bound on the
# remaining cost.
MIN_STEP_COST = {
    'steps': 1,
    'scrabble': min(SCRABBLE_VALUES.values()),
    # the most frequent word in the dictionary gives the smallest (cheapest)
    # possible frequency cost.
    'frequency': frequency_cost(max(dictionary, key=dictionary.get)),
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
        initial = initial.lower()
        goal = goal.lower()

        # make sure arguments are legal, raising an error if any are bad.
        if cost not in ('steps', 'scrabble', 'frequency'):
            raise ValueError(f"cost must be 'steps', 'scrabble' or 'frequency', got {cost!r}")
        if len(initial) not in (3, 4):
            raise ValueError(f"initial word {initial!r} must have 3 or 4 letters")
        if len(initial) != len(goal):
            raise ValueError(f"initial {initial!r} and goal {goal!r} must be the same length")
        if initial not in dictionary:
            raise ValueError(f"initial word {initial!r} is not in the dictionary")
        if goal not in dictionary:
            raise ValueError(f"goal word {goal!r} is not in the dictionary")

        # set instance attributes ...
        super().__init__(initial, goal)
        self.cost = cost

    def actions(self, state):
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        for i in range(len(state)):
            for c in string.ascii_lowercase:
                if c != state[i]:
                    candidate = state[:i] + c + state[i + 1:]
                    if candidate in dictionary:
                        yield (i, c)

    def result(self, state, action):
        """ takes a state and an action and returns a new state """
        i, c = action
        return state[:i] + c + state[i + 1:]

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
            _, letter = action
            return c + SCRABBLE_VALUES[letter]
        else:  # 'frequency'
            return c + frequency_cost(state2)

    def __repr__(self):
        """" return a suitable string to represent this problem instance """
        return f"DC({self.initial!r}->{self.goal!r}, cost={self.cost!r})"

    def h(self, node):
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        hamming_distance = sum(a != b for a, b in zip(node.state, self.goal))
        return hamming_distance * MIN_STEP_COST[self.cost]
