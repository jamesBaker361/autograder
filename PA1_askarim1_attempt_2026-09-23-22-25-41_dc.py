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
scrabble = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1,
    'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 6,
    'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1,
    'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1,
    'u': 1, 'v': 4, 'w': 4, 'x': 6, 'y': 4, 'z': 10}
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

        # Check if lowercase
        if initial != initial.lower() or goal != goal.lower():
            raise ValueError("Must be lowercase")

        # Check if length is 3 or 4
        if len(initial) != len(goal):
            raise ValueError("Must be same length")
        else:
            if len(initial) not in [3,4] or len(goal) not in [3,4]:
                raise ValueError("Word must be 3 or 4 letters")

        # Check if words in dictionary
        if initial not in dictionary or goal not in dictionary:
            raise ValueError("Word must be in dictionary")

        # check cost
        if cost not in ['steps', 'scrabble', 'frequency']:
            raise ValueError("Cost must be 'steps', 'scrabble', or 'frequency'.")

        #pass
        # make sure arguments are legal, raising an error if any are bad.
        pass

    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        actions = []

        for i in range(len(state)):
            for char in 'abcdefghijklmnopqrstuvwxyz':
                # make sure to not incorrectly replace
                if char == state[i]:
                    continue

                # new word
                new_word = state[:i] + char + state[i+1:]

                # now check if the new_word in the dictionary
                if new_word in dictionary:
                    actions.append((i,char))

        return actions

    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        pos, character = action

        return state[:pos] + character + state[pos+1:]
        # pass

    def goal_test(self, state):
        #TODO: complete this
        """ returns True iff state is a goal state for this problem instance """
        return state == self.goal
        # pass

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
            pos, character = action
            return c + scrabble[character]
        elif self.cost == 'frequency':
            return c + 1 + dictionary[state2]
            
        #pass

    def __repr__(self):
        #TODO: complete this
        """" return a suitable string to represent this problem instance """
        return f"dc({self.initial},{self.goal},{self.cost})"
        #pass

    def h(self, node):
        #TODO: complete this
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        state = node.state

        if self.cost == 'steps':
            estimate = 0

            for i in range(len(state)):
                if state[i] != self.goal[i]:
                    estimate += 1
            return estimate

        elif self.cost == 'scrabble':
            estimate = 0

            for i in range(len(state)):
                if state[i] != self.goal[i]:
                    estimate += scrabble[self.goal[i]]
            return estimate

        elif self.cost == 'frequency':
            estimate = 0

            for i in range(len(state)):
                if state[i] != self.goal[i]:
                    estimate += 1
            return estimate
        
        #pass
