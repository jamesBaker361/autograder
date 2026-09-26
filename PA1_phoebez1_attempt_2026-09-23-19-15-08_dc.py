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

scrabble_cost = {'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1, 'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1, 
                 'd': 2, 'g': 2, 
                 'b': 3, 'c': 3, 'm': 3, 'p': 3, 
                 'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4, 
                 'k': 5, 
                 'j': 6, 'x': 6, 
                 'q': 10, 'z': 10,}

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

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
        # makes everything lowercase
        initial = initial.lower()
        goal = goal.lower()
        
        # set instance attributes ...
        self.initial = initial
        self.goal = goal
        self.cost = cost

        # make sure arguments are legal, raising an error if any are bad.
        
        # checks if the words doesn't contain either three or four letters
        if len(initial) != 3 and len(initial) != 4:
            raise ValueError("Initial: Doesn't contain either three or four letters")
        if len(goal) != 3 and len(goal) != 4:
            raise ValueError("Goal: Doesn't contain either three or four letters")

        # checks if the words have the same length
        if len(initial) != len(goal):
            raise ValueError("Initial and goal doesn't have the same length")

        # checks if the words appear in the provided dictionary
        if initial not in dictionary:
            raise ValueError("Initial: Doesn't appear in the provided dictionary")
        if goal not in dictionary:
            raise ValueError("Goal: Doesn't appear in the provided dictionary")

        # checks if the cost argument is one of the three supported values
        if cost != 'steps' and cost != 'scrabble' and cost != 'frequency':
            raise ValueError("Cost argument must be one of the three supported values")

    def actions(self, state):
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        next_actions = []

        # loops through each position in the state (word)
        for i in range(len(state)):
            # loops through to change exactly one position
            for j in ALPHABET:
                # checks if the characters are the same
                if j == state[i]:
                    continue

                # replaces the existing character with a different character
                before = state[:i]
                after = state[i + 1:]
                new_word = before + j + after

                # checks if the new word is in the dictionary
                if new_word in dictionary:
                    next_actions.append((i, j))

        return next_actions

    def result(self, state, action):
        """ takes a state and an action and returns a new state """

        position = action[0]
        letter = action[1]
 
        before = state[:position]
        after = state[position + 1:]
        new_state = before + letter + after

        return new_state

    def goal_test(self, state):
        """ returns True iff state is a goal state for this problem instance """

        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """

        # letter used in actions function
        letter = action[1]

        if self.cost == 'steps':
            return c + 1

        if self.cost == 'scrabble':
            letter_value = scrabble_cost[letter]
            return c + letter_value

        if self.cost == 'frequency':
            rarity = dictionary[state2]
            return c + 1 + rarity

    def __repr__(self):
        """" return a suitable string to represent this problem instance """

        return "dc(" + self.initial + ", " + self.goal + ", " + self.cost + ")"

    def h(self, node):
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        state = node.state

        different = []

        # loops through every position
        for i in range(len(state)):
            # checks if the initial letter is different from the goal letter
            if state[i] != self.goal[i]:
                different.append(i)

        if self.cost == 'steps' or self.cost == 'frequency':
            return len(different)

        if self.cost == 'scrabble':
            total = 0

            for i in different:
                goal_letter = self.goal[i]
                total = total + scrabble_cost[goal_letter]

            return total
