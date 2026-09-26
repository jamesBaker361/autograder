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
        # Input Validation for Inital and Goal
        if not isinstance(initial, str) or not initial.islower():
            raise ValueError("Inital must be a lowercase string.")
        if not isinstance(goal, str) or not goal.islower():
            raise ValueError("Goal must be a lowercase string.")
        if len(initial) not in (3, 4):
            raise ValueError("Inital must be a 3 or 4 letter word.")
        if len(goal) not in (3, 4):
            raise ValueError("Goal must be a 3 or 4 letter word.")
        if len(initial) != len(goal):
            raise ValueError("Inital and Goal word length must be the same.")
        if initial not in dictionary:
            raise ValueError("Inital Word does not belong to the dictionary.")
        if goal not in dictionary:
            raise ValueError("Goal Word does not belong to the dictionary.")
        
        # Input Validation for Cost
        if cost not in ("steps", "scrabble", "frequency"):
            raise ValueError('Cost type given is not valid. Must be "steps", "scrabble", or "frequency"')

        # Set Variables if they pass input validation
        self.initial = initial
        self.goal = goal
        self.cost = cost

    def actions(self, state):
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        # Actions is a pair Ex (i, letter)
        # i is the position of the letter that will change
        # letter is the replacement at that position
        actions = []

        for i in range(len(state)):
            for letter in "abcdefghijklmnopqrstuvwxyz":
                if letter != state[i]:
                    # Copy everything before index i
                    # Insert letter
                    # Copy everything after index i
                    new_word = state[:i] + letter + state[i+ 1:]

                    # Check if this "word" is valid
                    # If it is then append to actions
                    if new_word in dictionary:
                        actions.append((i, letter))

        return actions

    def result(self, state, action):
        """ takes a state and an action and returns a new state """

        # Grab information from action
        position, letter = action

        # Modify the State and Return
        return(state[:position] + letter + state[position + 1:])

    def goal_test(self, state):
        """ returns True iff state is a goal state for this problem instance """

        return(state == self.goal)

    def path_cost(self, c, state1, action, state2):
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """

        # Case 1 steps
        if self.cost == "steps":
            return c + 1

        # Case 2 scrabble
        elif self.cost == "scrabble":
            scrabble_cost = {
                'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1, 'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
                'd': 2, 'g': 2,
                'b': 3, 'c': 3, 'm': 3, 'p': 3,
                'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
                'k': 5,
                'j': 6, 'x': 6,
                'q': 10, 'z': 10
            }

            position, letter = action
            return c + scrabble_cost[letter]

        # Case 3 frequency
        elif self.cost == "frequency":
            return c + 1 + dictionary[state2]

    def __repr__(self):
        """" return a suitable string to represent this problem instance """
        return (f"dc({self.initial},{self.goal},{self.cost})")

    def h(self, node):
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        state = node.state
        # Check for Goal
        if state == self.goal:
            return 0

        # Scrabble Costs
        scrabble_cost = {
            'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1, 'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
            'd': 2, 'g': 2,
            'b': 3, 'c': 3, 'm': 3, 'p': 3,
            'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
            'k': 5,
            'j': 6, 'x': 6,
            'q': 10, 'z': 10
        }

        # Case 1 Steps
        # Starts at 0 Every Wrong Letter is +1
        if (self.cost == 'steps'):
            sum = 0
            counter = -1
            for i in state:
                counter += 1
                if i != self.goal[counter]:
                    sum += 1
            return(sum)

        # Case 2 Scrabble
        # Simply the problem such that we ignore the rule that the word must be in the dictionary given
        # The cost is thus the direct letter changes needed
        # For example dog to cat would cost 3+1+1
        # Changing d to c, o to a, g to t.
        elif (self.cost == 'scrabble'):
            sum = 0
            counter = -1
            for i in state:
                counter += 1
                if i != self.goal[counter]:
                    sum += scrabble_cost[self.goal[counter]]
            return(sum)

        # Case 3 Frequency
        # Cost of Frequency is 1 + rarity(w)
        # Thus every action cost atleast 1
        # Simply and assume action cost is 1
        elif (self.cost == 'frequency'):
            sum = 0
            counter = -1
            for i in state:
                counter += 1
                if i != self.goal[counter]:
                    sum += 1
            return(sum)