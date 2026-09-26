""" starter file for pa1: dogcat """

import search       # AIMA module for search problems
import gzip         # read from a gzip'd file
import string

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
        #TODO: complete this
        # set instance attributes ...

        # make sure arguments are legal, raising an error if any are bad.
        if initial not in dictionary or len(initial) != len(goal) or not initial.islower() or not goal.islower() or len(initial) < 3 or len(initial) > 4:
            raise ValueError("Invalid initial value")
        self.initial = initial
        if goal not in dictionary :
            raise ValueError("Invalid goal value")
        self.goal = goal
        if cost not in ("steps", "scrabble", "frequency") :
            raise ValueError("Invalid cost type")
        self.cost = cost


    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """
        length = len(state)
        actions = []
        lowercase_alphabet = list(string.ascii_lowercase)
        for i in range(length) :
            cur_char = state[i]
            for char in lowercase_alphabet :
                if char != cur_char :
                    new_word = state[:i] + char + state[i + 1:]
                    if new_word in dictionary :
                        actions.append((i, char))
        return actions

    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        pos = action[0]
        char = action[1]
        new_state = state[:pos] + char + state[pos + 1:]
        return new_state

    def goal_test(self, state):
        #TODO: complete this
        """ returns True iff state is a goal state for this problem instance """
        if state == self.goal :
            return True
        return False

    def path_cost(self, c, state1, action, state2):
        #TODO: complete this
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """
        scrabble_costs = {"a":1, "e":1, "i":1, "o":1, "u":1, "l":1, "n":1, "s":1, "t":1, "r":1,
                          "d":2, "g":2,
                          "b":3, "c":3, "m":3, "p":3,
                          "f":4, "h":4, "v":4, "w":4, "y":4,
                          "k":5,
                          "j":6, "x":6,
                          "q":10, "z":10
                          }
        if self.cost == "steps" :
            c += 1
        elif self.cost == "scrabble" :
            c += scrabble_costs[action[1]]
        elif self.cost == "frequency" :
            c += 1 + dictionary[state2]
        return c

    def __repr__(self):
        #TODO: complete this
        """" return a suitable string to represent this problem instance """
        return "Initial Word: " + self.initial + "; Goal Word: " + self.goal + "; Cost measure: " + self.cost + ";"

    def h(self, node):
        #TODO: complete this
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        heuristic_score = 0
        scrabble_costs = {"a": 1, "e": 1, "i": 1, "o": 1, "u": 1, "l": 1, "n": 1, "s": 1, "t": 1, "r": 1,
                          "d": 2, "g": 2,
                          "b": 3, "c": 3, "m": 3, "p": 3,
                          "f": 4, "h": 4, "v": 4, "w": 4, "y": 4,
                          "k": 5,
                          "j": 6, "x": 6,
                          "q": 10, "z": 10
                          }
        if node.state == self.goal :
            heuristic_score = 0

        if self.cost == "steps" :
            for i in range(len(node.state)) :
                if (node.state[i] != self.goal[i]) :
                    heuristic_score += 1

        elif self.cost == "scrabble" :
            for i in range(len(node.state)) :
                if (node.state[i] != self.goal[i]) :
                    heuristic_score += scrabble_costs[self.goal[i]]

        elif self.cost == "frequency" :
            for i in range(len(node.state)) :
                if (node.state[i] != self.goal[i]) :
                    heuristic_score += 1
            if heuristic_score > 0:
                # 1 per mismatch + guaranteed rarity of landing on goal
                return heuristic_score + dictionary[self.goal]
        return heuristic_score