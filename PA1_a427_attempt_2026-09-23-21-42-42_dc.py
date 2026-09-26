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
        #TODO: complete this
        # set instance attributes ...

        self.initial = initial.lower()
        self.default_goal = goal.lower()
        self.cost = cost.lower()
        
        # make sure arguments are legal, raising an error if any are bad.
        initialSize = len(self.initial)

        if not self.initial or not self.default_goal:
            raise TypeError("Invalid word used")

        elif len(self.initial) != len(self.default_goal):
            raise ValueError("The length of either words are not the same")

        elif initialSize not in (3, 4):
            raise ValueError("The size of word isn't 3 nor 4")

        if self.cost not in ('steps', 'scrabble', 'frequency'):
            raise ValueError("The cost isn't steps, scrabble nor frequency")

        if self.initial not in dictionary or self.default_goal not in dictionary:
            raise ValueError("The initial word or the goal word isn't in the list")

    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        alphabet = list("abcdefghijklmnopqrstuvwxyz")
        actionList = []

        for letterPos in range(len(state)):
            currentWord = state

            if state[letterPos] != self.default_goal[letterPos]:
                for letter in alphabet:
                    currentWord = state[:letterPos] + letter + state[letterPos + 1:]
                    if currentWord in dictionary and currentWord != state:
                        actionList.append((letterPos, letter))

        return actionList
    
    def result(self, state, action):
            #TODO: complete this
            """ takes a state and an action and returns a new state """
            # Action is an index of the word
            index, letter = action
            state = state[:index] + letter + state[index + 1:]
            return state
    
    def goal_test(self, state):

        """ returns True iff state is a goal state for this problem instance """
        return state == self.default_goal

    def path_cost(self, c, state1, action, state2):
        #TODO: complete this
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """

        if self.cost == "steps":
            return c + 1

        elif self.cost == "scrabble":
            position, letter = action
            if letter in "aeioulnstr":
                return c + 1

            elif letter in "dg":
                return c + 2
            
            elif letter in "bcmp":
                return c + 3

            elif letter in "fhvwy": 
                return c + 4
                
            elif letter in "k":
                return c + 5
            
            elif letter in "jx":
                return c + 6

            else:
                return c + 10
            
        elif self.cost == "frequency":
            if state2 in dictionary:
                return c + 1 + dictionary[state2]
        

    def __repr__(self):
        #TODO: complete this
        """" return a suitable string to represent this problem instance """
        return f"DC(" + self.initial + ", " + self.default_goal + ", " + self.cost + ")"

    def h(self, node):
        
        cost = 0

        if self.cost == "steps":
            for i in range(len(node.state)):
                if node.state[i] != self.default_goal[i]:
                    cost += 1

        elif self.cost == "scrabble":
            for i in range(len(node.state)):
                if node.state[i] != self.default_goal[i]:
                    letter = self.default_goal[i]

                    if letter in "aeioulnstr":
                        cost += 1

                    elif letter in "dg":
                        cost += 2
                    
                    elif letter in "bcmp":
                        cost += 3

                    elif letter in "fhvwy": 
                        cost += 4
                        
                    elif letter in "k":
                        cost += 5
                    
                    elif letter in "jx":
                        cost += 6

                    else:
                        cost += 10

        elif self.cost == "frequency":
            for i in range(len(node.state)):
                if node.state[i] != self.default_goal[i]:
                    cost += 1

        return cost