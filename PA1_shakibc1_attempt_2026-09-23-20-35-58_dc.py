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

# Scrabble letter values
scrabble_values = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4,
    'i': 1, 'j': 6, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3,
    'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 6,
    'y': 4, 'z': 10
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
        if cost != 'steps' and cost != 'scrabble' and cost != 'frequency':
            raise ValueError("bad cost: " + str(cost))
        if len(initial) != len(goal):
            raise ValueError("initial and goal must be the same length")
        if not isinstance(initial, str) or not initial.isalpha() or not initial.islower():
            raise ValueError("initial word must be lowercase letters")
        if not isinstance(goal, str) or not goal.isalpha() or not goal.islower():
            raise ValueError("goal word must be lowercase letters")
        if len(initial) != 3 and len(initial) != 4:
            raise ValueError("words must be 3 or 4 letters")
        if initial not in dictionary:
            raise ValueError("initial word not in dictionary")
        if goal not in dictionary:
            raise ValueError("goal word not in dictionary")

    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        acts = []
        for i in range(len(state)):
            for ch in 'abcdefghijklmnopqrstuvwxyz':
                if ch == state[i]:
                    continue
                new_word = state[:i] + ch + state[i+1:]
                if new_word in dictionary:
                    acts.append((i, ch))
        return acts

    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        i = action[0]
        ch = action[1]
        return state[:i] + ch + state[i+1:]

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
            ch = action[1]
            return c + scrabble_values[ch]
        else:
            # frequency cost is 1 + rarity of the word you land on
            return c + 1 + dictionary[state2]

    def __repr__(self):
        #TODO: complete this
        """" return a suitable string to represent this problem instance """
        return f"DC({self.initial}, {self.goal}, {self.cost})"

    def h(self, node):
        #TODO: complete this
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        state = node.state
        if self.cost == 'steps':
            mismatches = 0
            for (t1, t2) in zip(state, self.goal):
                if t1 != t2:
                    mismatches += 1
            return mismatches

        elif self.cost == 'scrabble':
            total = 0
            for i in range(len(state)):
                if state[i] != self.goal[i]:
                    total += scrabble_values[self.goal[i]]
            return total
            
        else:
            if state == self.goal:
                return 0
            else:
                return 1 + dictionary[self.goal]
