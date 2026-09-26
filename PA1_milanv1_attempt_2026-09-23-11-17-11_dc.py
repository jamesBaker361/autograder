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
        # set instance attributes ...
        self.initial = initial
        self.goal = goal
        self.cost = cost
        # make sure arguments are legal, raising an error if any are bad.
        assert isinstance(initial, str) and isinstance(goal, str)
        assert len(initial) == len(goal)
        assert len(initial) == 3 or len(initial) == 4
        assert initial in dictionary and goal in dictionary
        assert cost in ('steps', 'scrabble', 'frequency')

    def actions(self, state):
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        possible_actions = []
        for position in range(len(state)):
            for letter in 'abcdefghijklmnopqrstuvwxyz':
                if letter != state[position]:
                    new_word = state[:position] + letter + state[position + 1:]
                    if new_word in dictionary:
                        possible_actions.append((position, letter))
        return possible_actions

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
            return c + 1

        if self.cost == 'frequency':
            return c + 1 + dictionary[state2]

        # For Scrabble, look at the one new letter in this action.
        letter = action[1]
        if letter in 'aeilnorstu':
            return c + 1
        elif letter in 'dg':
            return c + 2
        elif letter in 'bcmp':
            return c + 3
        elif letter in 'fhvwy':
            return c + 4
        elif letter == 'k':
            return c + 5
        elif letter in 'jx':
            return c + 6
        else:  # q or z
            return c + 10

    def __repr__(self):
        """" return a suitable string to represent this problem instance """
        return 'dc(' + self.initial + ',' + self.goal + ',' + self.cost + ')'

    def h(self, node):
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        different_positions = 0
        scrabble_total = 0

        for position in range(len(node.state)):
            if node.state[position] != self.goal[position]:
                different_positions = different_positions + 1

                # This goal letter must be inserted at least once.
                letter = self.goal[position]
                if letter in 'aeilnorstu':
                    scrabble_total = scrabble_total + 1
                elif letter in 'dg':
                    scrabble_total = scrabble_total + 2
                elif letter in 'bcmp':
                    scrabble_total = scrabble_total + 3
                elif letter in 'fhvwy':
                    scrabble_total = scrabble_total + 4
                elif letter == 'k':
                    scrabble_total = scrabble_total + 5
                elif letter in 'jx':
                    scrabble_total = scrabble_total + 6
                else:  # q or z
                    scrabble_total = scrabble_total + 10

        if self.cost == 'steps':
            return different_positions
        if self.cost == 'scrabble':
            return scrabble_total
        if different_positions == 0:
            return 0
        return different_positions + dictionary[self.goal]
