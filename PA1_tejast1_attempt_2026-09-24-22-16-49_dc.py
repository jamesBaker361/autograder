""" starter file for pa1: dogcat """

import search       # AIMA module for search problems
import gzip         # read from a gzip'd file

# file name for the dictionary, with one word per line.  Each line
# will have a word followed by a tab followed by a number, e.g.
#   and     0.07358445
#   for     0.18200336

dict_file = "words34.txt.gz"
MIN_LEN = 3
MAX_LEN = 4
VALID_COST = ["steps", "scrabble", "frequency"]
SCRABBLE = {
        "aeioulnstr" : 1,
        "dg" : 2,
        "bcmp" : 3,
        "fhvwy" : 4,
        "k" : 5,
        "jx" : 6,
        "qz" : 10,
        }
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
        
        if not ((initial.islower() and goal.islower()) and (initial.isalpha() and goal.isalpha())):
            raise ValueError("Words are not lowercase")
        if (len(initial) > MAX_LEN or len(goal) > MAX_LEN or len(initial) < MIN_LEN or len(goal) < MIN_LEN) or (len(initial) != len(goal)):
            raise ValueError("Words of incorrect length")
        if initial not in dictionary or goal not in dictionary:
            raise ValueError("Words not found in the dictionary")
        if cost not in VALID_COST:
            raise ValueError("Incorrect cost function provided")

        self.initial = initial
        self.goal = goal
        self.cost = cost


    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """
        states = []
        
        for i in range(len(state)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                curr = state[i]
                if c == curr:
                    continue
                if (state[:i]+c+state[i+1:]) not in dictionary:
                    continue
                states.append((i,c))
        return states
     

    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """ 
        i,c = action
        
        state = state[:i]+c+state[i+1:]
        return state
  

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
        
        if self.cost == "steps":
            return (c + 1) 
        elif self.cost == "scrabble":
            for key in SCRABBLE:
                if action[1] in key: 
                    return c + SCRABBLE[key]
        elif self.cost == "frequency":
            return (c + 1 + dictionary[state2])
    
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
        curr = node.state
        goal = self.goal
        D = 0
        scrabble_sum = 0

        for (s,g) in zip(curr, goal):
            if s != g:
                D += 1
                scrabble_sum += self.scrabble_value(g)

        if self.cost == "steps":
            return D
        elif self.cost == "scrabble":
            return scrabble_sum

        elif self.cost == "frequency":
            if D == 0:
                return 0
            else: 
                return D + dictionary[goal]


    def scrabble_value(self, letter):
        for key in SCRABBLE:
            if letter in key:
                return SCRABBLE[key]
