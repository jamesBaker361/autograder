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

SCRABBLE_VALUES = {
    'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1, 'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
    'd': 2, 'g': 2,
    'b': 3, 'c': 3, 'm': 3, 'p': 3,
    'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
    'k': 5,
    'j': 6, 'x': 6,
    'q': 10, 'z': 10,
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
       
        if initial not in dictionary:
            raise ValueError(f"{initial} is not a valid word")
        if goal not in dictionary:
            raise ValueError(f"{goal} is not a valid word")
        if len(initial) not in (3, 4):
            raise ValueError(f"{initial} must be 3 or 4 letters long")
        if len(goal) not in (3, 4):
            raise ValueError(f"{goal} must be 3 or 4 letters long")
        if len(initial) != len(goal):
            raise ValueError(f"{initial} and {goal} must be the same length")
        if cost not in ('steps', 'scrabble', 'frequency'):
            raise ValueError(f"cost must be steps, scrabble, or frequency, got {cost}")

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

        moves = []
        for pos in range(len(state)):
            for letter in 'abcdefghijklmnopqrstuvwxyz':
                word_letters = list(state)
                word_letters[pos] = letter
                new_word = ''.join(word_letters)
                if new_word in dictionary and new_word != state:
                    moves.append((pos, letter))
        return moves

    def result(self, state, action):
       
        """ takes a state and an action and returns a new state """
        pos, letter = action
        word_letters = list(state)
        word_letters[pos] = letter
        new_word = ''.join(word_letters)
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

        if self.cost == 'steps':
            return c + 1
        elif self.cost == 'scrabble':
            pos, letter = action
            return c + SCRABBLE_VALUES[letter]
        elif self.cost == 'frequency':
            return c + 1 + dictionary[state2]

    def __repr__(self):
        
        """" return a suitable string to represent this problem instance """

        return f"DC({self.initial} -> {self.goal}, cost={self.cost})"

    def h(self, node):
      
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        
        state = node.state
        goal = self.goal

        num = 0
        for i in range(len(state)):
            if state[i] != goal[i]:
                num += 1

        if num == 0:
            return 0

        if self.cost == 'steps':
            return num
        elif self.cost == 'scrabble':
            total = 0
            for i in range(len(state)):
                if state[i] != goal[i]:
                    total += SCRABBLE_VALUES[goal[i]]
            return total
        elif self.cost == 'frequency':
            return num + dictionary[goal]
