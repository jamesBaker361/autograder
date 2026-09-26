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

scrabble = {
    'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1, 'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
    'd': 2, 'g': 2,
    'b': 3, 'c': 3, 'm': 3, 'p': 3,
    'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
    'k': 5,
    'j': 6, 'x': 6,
    'q': 10, 'z': 10
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
        
        # make sure arguments are legal, raising an error if any are bad.
        if (len(initial) != len(goal) or len(initial) not in [3, 4]):
            raise ValueError("Initial and goal words must be the same length and either 3 or 4 letters long.")
        
        if (cost not in ['steps', 'scrabble', 'frequency']):
            raise ValueError("Cost argument not supported. Please choose between 'steps', 'scrabble' or 'frequency'.")

        if (not initial.isalpha() or not goal.isalpha() or not initial.islower() or not goal.islower()):
            raise ValueError("Initial/Goal arguments must be in the form of lowercase alphabetical strings.")
        
        if (initial not in dictionary or goal not in dictionary):
            raise ValueError("Initial and goal words must be in the dictionary.")
        
        # set instance attributes ...
        super().__init__(initial, goal)
        self.cost = cost

    
    


    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        alphabet = list(string.ascii_lowercase)

        actions = []

        # For each index (char) of the word:
        for i in range(len(state)):

            # We will try to replace it with every letter of the alphabet:
            for c in alphabet:
                temp_word = state[:i] + c + state[i+1:]

                # If the replacement produces a word that is in the dict, and not the state word, it is added to temp_actions
                if (temp_word != state and temp_word in dictionary):
                    actions.append((i,c))

        return actions


        

    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        i = action[0]
        c = action[1]

        return state[:i] + c + state[i+1:]

    def goal_test(self, state):
        #TODO: complete this
        """ returns True iff state is a goal state for this problem instance """

        if (state == self.goal):
            return True
        else:
            return False
        pass

    def path_cost(self, c, state1, action, state2):
        #TODO: complete this

        match self.cost:

            case "steps":
                return c + 1
            case "scrabble":
                return c + scrabble[action[1]]
            case "frequency":
                return c + 1 + dictionary[state2]

        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """
        

    def __repr__(self):
        #TODO: complete this
        """" return a suitable string to represent this problem instance """

        return f"dc({self.initial},{self.goal},{self.cost})"

    def h(self, node):
        #TODO: complete this

        state = node.state
        if (state == self.goal): 
            return 0

        h = 0



        
        # Steps: How many mismatched slots
        # Frequency: Dict cost is always >= 1 (because it's 1 + rarity(w)) so a minimum would just be the # of mismatched slots
        if (self.cost == 'steps' or self.cost == 'frequency'):
            for i in range(len(state)):
                if (state[i] != self.goal[i]):
                    h += 1
            
        # Scrabble: Scrabble cost of perfectly swapping all mismatched slots
        if (self.cost == 'scrabble'):
            for i in range(len(state)):
                if (state[i] != self.goal[i]):
                    h += scrabble[self.goal[i]]

        return h
        

        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        pass