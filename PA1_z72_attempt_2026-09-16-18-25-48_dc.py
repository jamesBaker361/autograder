""" starter file for pa1: dogcat """

import search       # AIMA module for search problems
import gzip         # read from a gzip'd file

SCRABBLEVALS = {
    1 : ['a', 'e', 'i', 'o', 'u', 'l', 'n', 's', 't', 'r'],
    2 : ['d', 'g'],
    3 : ['b', 'c', 'm', 'p'],
    4 : ['f', 'h', 'v', 'w', 'y'],
    5 : ['k'],
    6 : ['j', 'x'],
    10 : ['q', 'z']
}

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
        self.initial = initial.lower()
        self.goal = goal.lower()
        self.cost = cost.lower()

        # verification

        if cost not in ['steps', 'scrabble', 'frequency']:
            print(f"ERROR: invalid cost metric")

        if self.initial not in dictionary or self.goal not in dictionary:
            print(f"ERROR: invalid words")  

        if (len(self.initial) != len(self.goal)) or (len(self.initial) not in [3,4]):
            print(f"ERROR: words must be 3 or 4 letters and same length")

    def actions(self, state):
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        valids = []

        # action is (index, new char)

        for i in range(len(state)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                if c != state[i]:
                    new_word = state[:i] + c + state[i+1:]
                    if new_word in dictionary:
                        valids.append((i, c))
                        print(f"valid: {new_word}")

        return valids

    def result(self, state, action):
        """ takes a state and an action and returns a new state """
        i, c = action
        new_word = state[:i] + c + state[i+1:]
        return new_word

    def goal_test(self, state):
        """ returns True iff state is a goal state for this problem instance """
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """

        cost = self.cost

        if cost == 'steps':
            return c + 1
        elif cost == 'scrabble':
            for value, letters in SCRABBLEVALS.items():  
                if action[1] in letters:
                    return c + value
        elif cost == 'frequency':
            return c + 1 + dictionary[state2]

    def __repr__(self):
        """" return a suitable string to represent this problem instance """
        return f"DOGCAT | INIT:{self.initial}, GOAL:{self.goal}, COST:{self.cost}"

    def h(self, node):
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        state = node.state
        errors = 0
        scrabbleCost = 0

        for index in range(len(state)):
            if state[index] != self.goal[index]:
                # number of non matching letters up to n
                errors += 1

                for value, letters in SCRABBLEVALS.items():
                    if self.goal[index] in letters:
                        scrabbleCost += value
                        break

        if self.cost == 'steps':
            return errors
        elif self.cost == 'scrabble':
            return scrabbleCost
        elif self.cost == 'frequency':
            return errors
