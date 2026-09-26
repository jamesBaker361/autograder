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
        if not isinstance(initial, str) or not isinstance(goal, str):
            raise ValueError("Initial and goal must be strings.")

        if not (initial.isascii() and initial.isalpha() and initial.islower()):
            raise ValueError("Initial word must contain only lowercase letters.")

        if not (goal.isascii() and goal.isalpha() and goal.islower()):
            raise ValueError("Goal word must contain only lowercase letters.")

        if len(initial) not in (3, 4) or len(goal) not in (3, 4):
            raise ValueError("Initial and goal must have 3 or 4 letters.")

        if len(initial) != len(goal):
            raise ValueError("Initial and goal must have the same length.")

        if initial not in dictionary or goal not in dictionary:
            raise ValueError("Initial and goal must be in the dictionary.")

        if cost not in ('steps', 'scrabble', 'frequency'):
            raise ValueError("Invalid cost method.")

        super().__init__(initial, goal)

        self.cost = cost



    def actions(self, state):
        """ Given a state (i.e., a word), return a list or iterator of
            all possible next actions.  An action is defined by position
            in the word and a character to put in that position.  But the
            result must be a legal word, i.e., in our dictionary, and it
            should not be the same as the state, i.e., don't replace a
            character with the same character """
        
        legal_actions = []

        for position in range(len(state)):
            for letter in 'abcdefghijklmnopqrstuvwxyz':
                if letter == state[position]:
                    continue
                new_word = (
                    state[:position]
                    + letter
                    + state[position + 1:]
                )
                if new_word in dictionary:
                    legal_actions.append((position, letter))
        return legal_actions
    

    def result(self, state, action):
        """ takes a state and an action and returns a new state """
        position, letter = action
        new_state = (
            state[:position]
            + letter
            + state[position + 1:]
        )
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
        if self.cost == 'steps':
            return c + 1

        elif self.cost == 'scrabble':

            scrabble_values = {
                'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1,
                'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
                'd': 2, 'g': 2,
                'b': 3, 'c': 3, 'm': 3, 'p': 3,
                'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
                'k': 5,
                'j': 6, 'x': 6,
                'q': 10, 'z': 10
            }

            position, letter = action

            return c + scrabble_values[letter]

        elif self.cost == 'frequency':
            return c + 1 + dictionary[state2]

    def __repr__(self):
        """" return a suitable string to represent this problem instance """
        return f"dc({self.initial},{self.goal},{self.cost})"

    def h(self, node):
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        state = node.state
        distance = sum(
            1 for current, goal in zip(state, self.goal)
            if current != goal
        )
        if distance == 0:
            return 0
        if self.cost == 'steps':
            return distance
        elif self.cost == 'scrabble':
            scrabble_values = {
                'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1,
                'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
                'd': 2, 'g': 2,
                'b': 3, 'c': 3, 'm': 3, 'p': 3,
                'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
                'k': 5,
                'j': 6, 'x': 6,
                'q': 10, 'z': 10
            }

            total = 0

            for current, goal in zip(state, self.goal):
                if current != goal:
                    total += scrabble_values[goal]
            return total

        elif self.cost == 'frequency':
            return distance + dictionary[self.goal]
