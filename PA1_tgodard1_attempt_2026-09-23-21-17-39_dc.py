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

        if not isinstance(initial, str) or not initial.isascii() \
                or not initial.isalpha() or not initial.islower():
            raise ValueError("Initial Must be a lowercase string of letters")

        if len(initial) not in (3, 4):
            raise ValueError("Initial Must contain three or four letters")

        if initial not in dictionary:
            raise ValueError("Initial Must be in the dictionary")

        if not isinstance(goal, str) or not goal.isascii() \
                or not goal.isalpha() or not goal.islower():
            raise ValueError("Goal Must be a lowercase string of letters")
        
        if len(goal) not in (3, 4):
            raise ValueError("Goal Must contain three or four letters")
        
        if goal not in dictionary:
            raise ValueError("Goal Must be in the dictionary")

        if len(initial) != len(goal):
            raise ValueError("Initial and goal must have the same length")

        if cost not in ('steps', 'scrabble', 'frequency'):
            raise ValueError("Cost must be 'steps', 'scrabble', or 'frequency'")

        super().__init__(initial, goal)
        self.cost = cost

    def actions(self, state):
        actions = []

        for i in range(len(state)):
            for letter in 'abcdefghijklmnopqrstuvwxyz':
                if letter == state[i]:
                    continue

                new_word = state[:i] + letter + state[i + 1:]

                if new_word in dictionary:
                    actions.append((i, letter))

        return actions

    def result(self, state, action):
        """ takes a state and an action and returns a new state """

        position, letter = action

        return state[:position] + letter + state[position + 1:]

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
            action_cost = 1

        elif self.cost == 'scrabble':
            action_cost = SCRABBLE_VALUES[action[1].upper()]

        else:
            action_cost = 1 + dictionary[state2]
        return c + action_cost

    def __repr__(self):
        """" return a suitable string to represent this problem instance """

        return f"DC({self.initial} -> {self.goal}, cost={self.cost})"

    def h(self, node):
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        state = node.state
        mismatches = 0

        for index in range(len(state)):
            if state[index] != self.goal[index]:
                mismatches += 1

        if self.cost == 'scrabble':
            estimate = 0
            for index in range(len(state)):
                if state[index] != self.goal[index]:
                    estimate += SCRABBLE_VALUES[self.goal[index].upper()]
            return estimate

        elif self.cost == 'frequency':
            minimum_rarity = min(dictionary.values())
            return mismatches * (1 + minimum_rarity)

        return mismatches


SCRABBLE_VALUES = {
    'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1,
    'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 6,
    'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1,
    'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1,
    'U': 1, 'V': 4, 'W': 4, 'X': 6, 'Y': 4,
    'Z': 10
}
