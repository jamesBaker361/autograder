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

# letter values for the scrabble cost measure, stored easily
SCRABBLE = {}
for letters, value in [('aeioulnstr', 1), ('dg', 2), ('bcmp', 3), ('fhvwy', 4),
                       ('k', 5), ('jx', 6), ('qz', 10)]:
    for letter in letters:
        SCRABBLE[letter] = value

MIN_RARITY = min(dictionary.values()) #min rarity of any word

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

        for name, word in (('initial', self.initial), ('goal', self.goal)):
            if not isinstance(word, str):
                raise TypeError(f"{name} word must be a string, got {word!r}")
            if not word.islower():
                raise ValueError(f"{name} word must be lowercase: {word!r}")
            if len(word) not in (3, 4):
                raise ValueError(f"{name} word must have 3 or 4 letters")
            if word not in dictionary:
                raise ValueError(f"{name} word is not in the dictionary: {word!r}")

        if self.cost not in ('steps', 'scrabble', 'frequency'):
            raise ValueError(f"cost must be 'steps', 'scrabble', or 'frequency', not what you chose")
        if len(self.initial) != len(self.goal):
            raise ValueError(f"initial and goal must be the same length: {initial!r}, {goal!r}")
        

    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """
        acts = [] #list
        for i, old_char in enumerate(state): #gives each position with letter currently there
            for c in string.ascii_lowercase: #set to 
                if c == old_char:
                    continue                     # same letter is just same word,so skip
                new_word = state[:i] + c + state[i+1:] #everything before and after i plus the character c
                if new_word in dictionary:
                    acts.append((i, c)) # add valid new word to list, excluding the old word
        return acts
        

    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        i, c = action # i is position, c is letter character
        return state[:i] + c + state[i+1:] #adds everything before i and after i plus the new letter character that action has

        

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
            i, letter = action
            return c + SCRABBLE[letter] #c plus cost of letter based on scrabble
        else:
            return c + 1 + dictionary[state2]


    def __repr__(self):
        #TODO: complete this
        """" return a suitable string to represent this problem instance """
        return f"dc({self.initial},{self.goal},{self.cost})"

    def h(self, node):
        #TODO: complete this
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        state = node.state #the word
        diffs = []
        for i in range(len(state)):          
            if state[i] != self.goal[i]:     # letters differ at this position?
                diffs.append(i)              # remember the position

        k = len(diffs) #minimum number of moves left determined by the amount of wrong letters found

        if k == 0:
            return 0 #goal state
        if self.cost == 'steps':
            return k
        elif self.cost == 'scrabble':
            return sum(SCRABBLE[self.goal[i]] for i in diffs) 
        else:
            return (1 + dictionary[self.goal]) + (k - 1) * (1 + MIN_RARITY)

