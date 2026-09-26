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


# SCRABBLE COST PAIRS
SCRABBLE_VALUES = {
    'a': 1,
    'b': 3,
    'c': 3,
    'd': 2,
    'e': 1,
    'f': 4,
    'g': 2,
    'h': 4,
    'i': 1,
    'j': 6,
    'k': 5,
    'l': 1,
    'm': 3,
    'n': 1,
    'o': 1,
    'p': 3,
    'q': 10,
    'r': 1,
    's': 1,
    't': 1,
    'u': 1,
    'v': 4,
    'w': 4,
    'x': 6,
    'y': 4,
    'z': 10
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
        # make sure arguments are legal, raising an error if any are bad.

        # string
        if not isinstance(initial, str):
            raise ValueError("start word must be a string")


        if not isinstance(goal, str):
            raise ValueError("goal word must be a string")

        # lowercase
        if initial != initial.lower():

            raise ValueError("start word must be lowercase")

        if goal != goal.lower():
            raise ValueError("goal word must be lowercase")

        # length
        if len(initial) not in (3, 4):
            raise ValueError("start must only be 3 or 4 letters")

        if len(goal) not in (3, 4):
            raise ValueError("goal word must only be 3 or 4 letters")

        # same string length
        if len(initial) != len(goal):
            raise ValueError("start and goal words not the same length")

        # alphabetic
        if not initial.isalpha():

            raise ValueError("start word must contain only letters")

        if not goal.isalpha():
            raise ValueError("goal word must contain only letters")

        # confirm in list of words
        if initial not in dictionary:
            raise ValueError(f"start word '{initial}' is not in dictionary")

        if goal not in dictionary:
            raise ValueError(f"goal word '{goal}' is not in dictionary")

        # cost method is 1 of the 3 listed
        if cost not in ('steps', 'scrabble', 'frequency'):
            raise ValueError("cost must be either 'steps', 'scrabble', or 'frequency'")

        self.initial = initial
        self.goal = goal
        self.cost = cost


    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        actions = []


        for position in range(len(state)):


            for letter in 'abcdefghijklmnopqrstuvwxyz':


                if letter == state[position]:
                    continue

                new_state = (
                    state[:position]
                    + letter
                    + state[position + 1:]
                )

                if new_state in dictionary:
                    actions.append((position, letter))

        return actions

    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """

        position, letter = action

        return (
            state[:position]
            + letter
            + state[position + 1:]
        )

    def goal_test(self, state):
                #TODO: complete this
        """ returns True iff state is a goal state for this problem instance """

        return state == self.goal

    def path_cost(self, c, state1, action, state2):
                #TODO: complete this
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """

        if self.cost == 'steps':
            return c + 1

        elif self.cost == 'scrabble':
            position, letter = action
            return c + SCRABBLE_VALUES[letter]

        elif self.cost == 'frequency':
            return c + 1 + dictionary[state2]

        # This should never be reached because __init__ validates cost.
        raise ValueError("Unknown cost method")

    def __repr__(self):
                #TODO: complete this
        """" return a suitable string to represent this problem instance """

        return f"dc({self.initial},{self.goal},{self.cost})"

    def h(self, node):
        #TODO: complete this
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        state = node.state

        # goal has 0 cost remaining
        if state == self.goal:
            return 0

        # position of start state goal that not matching goal state
        mismatches = []

        for i in range(len(state)):
            if state[i] != self.goal[i]:
                mismatches.append(i)


        if self.cost == 'steps':
            return len(mismatches)

        # SCRABBLE
        elif self.cost == 'scrabble':
            total = 0

            for i in mismatches:
                total += SCRABBLE_VALUES[self.goal[i]]

            return total

        # FREQUENCY
        elif self.cost == 'frequency':
            return len(mismatches)

        raise ValueError("Unknown cost method")