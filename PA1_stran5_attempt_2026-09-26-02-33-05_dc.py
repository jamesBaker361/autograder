"""
 * Title: dc.py
 * Project: CMSC 471 PA_1, Fall 2026
 * Author: Sarah Tran
 * Date: 09/23/2026
 * Section: 3
 * E-mail: stran5@umbc.edu
 * Description: Implements the DOGCAT word-changing problem using a
 * dictionary of valid words. Finds legal one-letter changes
 * to reach the goal word. Calculates path costs using steps,
 * Scrabble values, or word rarity. Uses heuristics to
 * estimate the remaining cost for A* search.
"""

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
        # Checks both initial and goal words are strings
        if not isinstance(initial, str) or not isinstance(goal, str):
            raise ValueError("Both words must be strings.")

        # Checks the initial and goal words are valid strings (in dictionary)
        if initial not in dictionary or goal not in dictionary:
            raise ValueError("Both words must be in the dictionary.")

        # Checks the initial and goal words are the same length
        if len(initial) != len(goal):
            raise ValueError("Both words must be the same length.")

        # Checks the initial and goal words are lowercase, contain 3 or 4 letters, 
        # and contain only ascii characters
        if not (initial.islower() and
                goal.islower() and
                len(initial) in [3, 4] and
                len(goal) in [3, 4] and
                initial.isascii() and
                goal.isascii()):
            raise ValueError("Both words must be lowercase and contain 3 or 4 letters.")

        # Checks the cost is a supported value
        if cost not in ('steps', 'scrabble', 'frequency'):
            raise ValueError("Cost must be one of: 'steps', 'scrabble', 'frequency'.")

        # Initializes the initial and goal words
        super().__init__(initial, goal)
        self.cost = cost


    def actions(self, state):
        valid_actions = []

        # Checks each position in the word
        for i in range(len(state)):

            # Checks each letter in the alphabet
            for letter in 'abcdefghijklmnopqrstuvwxyz':

                # Checks if the letter is the same as the current letter in the word
                if letter == state[i]:
                    continue

                # Creates a new word by replacing the letter at position i with the new letter
                new_word = state[:i] + letter + state[i+1:]

                # Checks if the new word is in the dictionary
                if new_word in dictionary:
                    valid_actions.append((i, letter))

        return valid_actions


    def result(self, state, action):
        # Stores the position and letter from the action tuple
        position, letter = action

        # Returns word after replacing that letter
        return state[:position] + letter + state[position + 1:]

    # Returns True if the state is the goal state, False otherwise
    def goal_test(self, state):
        return state == self.goal


    def path_cost(self, c, state1, action, state2):
        # Adds 1 to the cost for each step taken
        if self.cost == 'steps':
            return c + 1

        # Cost depends on the replacement letter
        elif self.cost == 'scrabble':
            scores = {'a': 1, 'b': 3, 'c': 3, 'd': 2,
                'e': 1, 'f': 4, 'g': 2, 'h': 4,
                'i': 1, 'j': 6, 'k': 5, 'l': 1,
                'm': 3, 'n': 1, 'o': 1, 'p': 3,
                'q': 10, 'r': 1, 's': 1, 't': 1,
                'u': 1, 'v': 4, 'w': 4, 'x': 6,
                'y': 4, 'z': 10 }

            position, letter = action
            return c + scores[letter]

        # Adds 1 to the cost for each step taken and adds the rarity of the new word
        elif self.cost == 'frequency':
            return c + 1 + dictionary[state2]


    def __repr__(self):
        return "dc(" + self.initial + "," + self.goal + "," + self.cost + ")"

    
    def h(self, node):
        total = 0
        state = node.state

        # Finds the positions where the current state differs from the goal state
        differences = []

        # Loops through the state and compares to the corresponding character in the goal state
        for i in range(len(state)):
            if state[i] != self.goal[i]:
                differences.append(i)

        # At least one move per incorrect position (steps)
        if self.cost == 'steps':
            return len(differences)

        # Cost of the required goal letters (scrabble)
        elif self.cost == 'scrabble':
            scores = {
                'a': 1, 'b': 3, 'c': 3, 'd': 2,
                'e': 1, 'f': 4, 'g': 2, 'h': 4,
                'i': 1, 'j': 6, 'k': 5, 'l': 1,
                'm': 3, 'n': 1, 'o': 1, 'p': 3,
                'q': 10, 'r': 1, 's': 1, 't': 1,
                'u': 1, 'v': 4, 'w': 4, 'x': 6,
                'y': 4, 'z': 10
            }

            for i in differences:
                letter = self.goal[i]
                total = total + scores[letter]

            return total

        # Min steps plus goal's rarity (frequency)
        elif self.cost == 'frequency':
            if len(differences) == 0:
                return 0
            return len(differences) + dictionary[self.goal]

