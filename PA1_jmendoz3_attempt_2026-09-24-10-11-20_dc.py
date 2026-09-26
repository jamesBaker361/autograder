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

scrabble_cost = {'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1,
                          'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
                          'd': 2, 'g': 2,
                          'b': 3, 'c': 3, 'm': 3, 'p': 3,
                          'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
                          'k': 5,
                          'j': 6, 'x': 6,
                          'q': 10, 'z': 10,}
        

# print(dictionary.keys())

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
        self.initial = initial.lower()
        self.goal = goal.lower()
        self.cost = cost
        pass
        # make sure arguments are legal, raising an error if any are bad.
        if len(self.initial) != len(self.goal):
            raise ValueError('initial and goal state must be the same length')
        elif len(self.initial) < 3 or len(self.initial) > 4:
            raise ValueError('specified initial and/or goal state must be 3 or 4 letters long')
        elif self.initial not in dictionary or self.goal not in dictionary:
                    print(self.initial)
                    print(self.goal)
                    print(self.initial in dictionary)
                    print(self.goal in dictionary)
                    raise ValueError('specified initial and/or goal state not in dictionary')
        elif self.cost != 'steps' and self.cost != 'frequency' and self.cost != 'scrabble':
             raise ValueError('invalid cost type')
        


    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """
        possible_actions = []

        # get length of word then turn into a list, as lists are mutable
        word_length = len(state)
        word_characters = list(state)
        word = state

        # checking all possible letters
        possible_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                            'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                            'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                            'y', 'z']

        # dog -> aog = X, bog = :), cog = :), skip dog, eog = X...
        # so for each letter in dog, replace it with all possible letters
        for i in range(word_length):
             for letter in possible_letters:
                if state[i] != letter: # get all letters except the letter being replaced
                    word_characters[i] = letter # hope that works
                    word = ''.join(word_characters) # turn back into string
                # check if the new word is in the dictionary     
                if word in dictionary and len(word) == word_length:
                       possible_actions.append((i, letter)) # a tuple representing the index being changed, and the letter
                    # reset the word for the next letter
                word = state
                word_characters = list(state)

        
        return possible_actions

    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        word = list(state)
        word[action[0]] = action[1] # in a tuple (x,y), x = the index being replaced & y = the letter
        word = ''.join(word)
        return word


    def goal_test(self, state):
        #TODO: complete this
        """ returns True iff state is a goal state for this problem instance """
        if self.goal == state:
             return True
        return False

    def path_cost(self, c, state1, action, state2):
        #TODO: complete this
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """
        
        if self.cost == 'steps':
             return c + 1
        elif self.cost == 'scrabble':
             return c + scrabble_cost[action[1]]
        elif self.cost == 'frequency':
             return c + 1 + dictionary[state2]
        pass

    def __repr__(self):
        #TODO: complete this
        """" return a suitable string to represent this problem instance """
        return f"DOGCAT({self.initial},{self.goal},{self.cost})"
        pass

    def h(self, node):
        #TODO: complete this
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        # each letter has a cost of one. so if two three letter words are completely
        # different, the minimum changes from the first to second word is 3.

        cost = 0
        state = node.state
        if self.cost == 'steps':
            for i in range(len(state)): # error checking already happened, safe to do this
                if state[i] != self.goal[i]:
                    cost += 1
            return cost
        elif self.cost == 'scrabble':
            for i in range(len(state)): # 
                if state[i] != self.goal[i]:
                    cost = cost + scrabble_cost[self.goal[i]]
            return cost
        elif self.cost == 'frequency':
            for i in range(len(state) - 1): # 
                # we do not know the path taken from the initial to goal state.
                # we do know that every path has a minimum cost of one. so while not
                # 100% accurate, it is safe to assume each move has a cost of at least 1
                if state[i] != self.goal[i]:
                    cost += 1
            cost = cost + dictionary[self.goal]
            return cost
        

