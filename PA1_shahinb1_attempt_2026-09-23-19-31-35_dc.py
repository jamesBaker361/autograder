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
        # set instance attributes
        self.initial = initial
        self.goal = goal
        self.cost = cost

        # make sure arguments are legal
        if not isinstance(initial, str) or not isinstance(goal, str):
            raise ValueError("Initial and goal must be strings")

        if initial != initial.lower() or goal != goal.lower():
            raise ValueError("Words must be lowercase")

        if len(initial) not in (3, 4) or len(goal) not in (3, 4):
            raise ValueError("Words must have 3 or 4 letters")

        if len(initial) != len(goal):
            raise ValueError("Initial and goal must have the same length")

        if initial not in dictionary or goal not in dictionary:
            raise ValueError("Initial and goal must be in the dictionary")

        if cost not in ('steps', 'scrabble', 'frequency'):
            raise ValueError("Invalid cost method")

    def actions(self, state):
        # Given a word, return a list or iterator of all possible next actions

        actions = []

        for i in range(len(state)):
            for letter in 'abcdefghijklmnopqrstuvwxyz':
                if letter != state[i]:
                    new_word = state[:i] + letter + state[i+1:]

                    if new_word in dictionary:
                        actions.append((i, letter))

        return actions

    def result(self, state, action):
        """ takes a state and an action and returns a new state """

        position, letter = action
        return state[:position] + letter + state[position+1:]

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
            letter = action[1]

            if letter in 'aeioulnstr':
                value = 1
            elif letter in 'dg':
                value = 2
            elif letter in 'bcmp':
                value = 3
            elif letter in 'fhvwy':
                value = 4
            elif letter == 'k':
                value = 5
            elif letter in 'jx':
                value = 6
            elif letter in 'qz':
                value = 10

            return c + value

        elif self.cost == 'frequency':
            return c + 1 + dictionary[state2]

    def __repr__(self):
        """ return a suitable string to represent this problem instance """

        return "dc({},{},{})".format(
            self.initial, self.goal, self.cost
        )

    def h(self, node):
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        state = node.state

        different = [
            i for i in range(len(state))
            if state[i] != self.goal[i]
        ]

        if len(different) == 0:
            return 0

        if self.cost == 'steps':
            return len(different)

        elif self.cost == 'scrabble':
            total = 0

            for i in different:
                letter = self.goal[i]

                if letter in 'aeioulnstr':
                    total += 1
                elif letter in 'dg':
                    total += 2
                elif letter in 'bcmp':
                    total += 3
                elif letter in 'fhvwy':
                    total += 4
                elif letter == 'k':
                    total += 5
                elif letter in 'jx':
                    total += 6
                elif letter in 'qz':
                    total += 10

            return total

        elif self.cost == 'frequency':
            return len(different) + dictionary[self.goal]
