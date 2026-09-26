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
        if not(initial.islower() and goal.islower()):
            raise ValueError("Initial or Goal is not all lowercase")
        if not(len(initial) == len(goal)):
            raise ValueError("Inital and Goal are not same length")
        if not((len(initial) == 4 or len(initial) == 3)):
            raise ValueError("Initial or Goal are not 3 to 4 letter words")
        if not(cost == "steps" or cost == "frequency" or cost == "scrabble"):
            raise ValueError("Cost measure is not valid")

        if initial in dictionary and goal in dictionary:
            super().__init__(initial, goal)
            self.cost = cost
        else:
            raise ValueError("Initial or Goal are not legal words")
    def actions(self, state):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        possible_next_actions = []
        for i in range(len(state)):
            for char in alphabet:
                if char != state[i]:
                    new_word = state[:i] + char + state[i+1:]
                    if new_word in dictionary:
                        possible_next_actions.append((i, char))
        return possible_next_actions
    def result(self, state, action):
        return state[:action[0]] + action[1] + state[action[0]+1:]
    def goal_test(self, state):
        return state == self.goal
    def path_cost(self, c, state1, action, state2):
        scrabble_scores = {
            'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1, 'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
            'd': 2, 'g': 2,
            'b': 3, 'c': 3, 'm': 3, 'p': 3,
            'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
            'k': 5,
            'j': 6, 'x': 6,
            'q': 10, 'z': 10
        }
        if self.cost == "steps":
            return c + 1
        if self.cost == "scrabble":
            return c + scrabble_scores[action[1]]
        if self.cost == "frequency":
            return c + 1 + dictionary[state2]
    def __repr__(self):
        return f"DC('{self.initial}' -> '{self.goal}', cost='{self.cost}')"
    def h(self, node):

        #if self.cost == "frequency":
            #base_h = sum(1 for i in range(len(node.state)) if node.state[i] != self.goal[i])
            #if node.state == self.goal:
                #return 0
            #else:
                #return base_h + dictionary[self.goal]
            
        scrabble_scores = {
            'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1, 'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
            'd': 2, 'g': 2,
            'b': 3, 'c': 3, 'm': 3, 'p': 3,
            'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
            'k': 5,
            'j': 6, 'x': 6,
            'q': 10, 'z': 10
        }
        heuristic = 0
        for i in range(len(node.state)):
            if node.state[i] != self.goal[i]:
                if self.cost == "steps" or self.cost == "frequency":
                    heuristic += 1
                elif self.cost == "scrabble":
                    heuristic += scrabble_scores[self.goal[i]]
        return heuristic