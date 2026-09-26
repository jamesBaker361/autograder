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
    

scrabble_costs = {
    'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1, 'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
    'd': 2, 'g': 2,
    'b': 3, 'c': 3, 'm': 3, 'p': 3,
    'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
    'k': 5,
    'j': 6, 'x': 6,
    'q': 10, 'z': 10
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
        self.initial = initial
        self.goal = goal
        self.cost = cost
        # make sure arguments are legal, raising an error if any are bad.
        if (initial.isupper() or goal.isupper()):
            raise ValueError("Words must be lowercase")
        if (initial not in dictionary or goal not in dictionary):
            raise ValueError("Initial or goal not in dictionary")
        if (len(initial) != len(goal)):
            raise ValueError("Words must be same length")

    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """
        chars = 'abcdefghijklmnopqrstuvwxyz'
        legal = []
        for i in range(len(state)):
            for c in chars:
                curr_word_list = list(state)
                if (curr_word_list[i] != c):
                    curr_word_list[i] = c
                new_word = "".join(curr_word_list)

                if new_word in dictionary:
                    legal.append((i, c))

        return legal

    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        # state = str
        # action = (index of char to change, new char)
        curr_word_list = list(state)
        curr_word_list[action[0]] = action[1]
        new_word = "".join(curr_word_list)
        return new_word

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
        if self.cost == "steps":
            return c + 1
        elif self.cost == "scrabble":
            return c + scrabble_costs[action[1]]
        elif self.cost == "frequency":
            return c + 1 + dictionary[state2]
        return c

    def __repr__(self):
        #TODO: complete this
        """" return a suitable string to represent this problem instance """
        return f"{self.initial, self.goal, self.cost}"

    def h(self, node):
        #TODO: complete this
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        state = node.state
        if state == self.goal:
            return 0

        numMismatches = 0
        for i in range(len(state)):
            if state[i] != self.goal[i]:
                numMismatches += 1

        if self.cost == "steps":
            return numMismatches
        elif self.cost == "scrabble":
            return sum(scrabble_costs[self.goal[i]] for i in range(len(state)) if state[i] != self.goal[i])
        elif self.cost == "frequency":
            return numMismatches + dictionary[self.goal]

        return 0
            
