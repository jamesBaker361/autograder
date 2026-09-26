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
        # set instance attributes ...
        # one of the cost measures: steps, scrabble, or frequency.
        costs = ["steps", "scrabble", "frequency"]
        if cost not in costs:
            raise ValueError("Cost not valid");
        # make sure arguments are legal, raising an error if any are bad.
        # be lowercase strings;
        # contain either three or four letters;
        # have the same length;
        if type(initial) is not str or type(goal) is not str:
            raise ValueError("Must be strings");
        if not (initial.islower() and goal.islower()):
            raise ValueError("Must be lowercase");
        if len(initial) not in [3,4]:
            raise ValueError("Must be same 3/4 chars");
        if len(initial) != len(goal):
            raise ValueError("Must be same length");

        # appear in the provided dictionary.
        if initial not in dictionary or goal not in dictionary:
            raise ValueError("Must appear in dictionary")

        # initialize problem
        super().__init__(initial, goal)
        self.cost = cost

    def actions(self, state):
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """
        
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        actions = []
        
        for i in range(len(state)):
            for char in alphabet:
                if char != state[i]:
                    # create the new word
                    new_word = state[:i] + char + state[i+1:]
                    
                    # if a real word, add to list
                    if new_word in dictionary:
                        actions.append((i, char))
                        
        return actions

    def result(self, state, action):
        """ takes a state and an action and returns a new state """
        # unpack action
        i, char = action
        
        # return new state
        return state[:i] + char + state[i+1:]

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
            # every cost is 1 for steps
            return c + 1
            
        elif self.cost == 'scrabble':
            # scrabble cost associated with letters
            scrabble = {
                'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1, 'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
                'd': 2, 'g': 2, 'b': 3, 'c': 3, 'm': 3, 'p': 3,
                'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4, 'k': 5,
                'j': 6, 'x': 6, 'q': 10, 'z': 10
            }
            
            # unpack action
            i, char = action
            
            # add scrabble cost
            return c + scrabble[char]

        elif self.cost == 'frequency':
            # cost is 1 + rarity of state2
            # dictionary holds rarity values
            return c + 1 + dictionary[state2]

    def __repr__(self):
        """" return a suitable string to represent this problem instance """
        return f"dc({self.initial}, {self.goal}, {self.cost})"

    def h(self, node):
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        state = node.state
        goal = self.goal
        heuristic = 0
        
        scrabble = {
            'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1, 'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
            'd': 2, 'g': 2, 'b': 3, 'c': 3, 'm': 3, 'p': 3,
            'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4, 'k': 5,
            'j': 6, 'x': 6, 'q': 10, 'z': 10
        }
        
        # loop through indexes
        for i in range(len(state)):
            # for this index
            if state[i] != goal[i]:
                
                if self.cost == 'steps':
                    # atleast 1 step
                    heuristic += 1
                    
                elif self.cost == 'scrabble':
                    # atleast pay for final letter
                    char = goal[i]
                    heuristic += scrabble[char]
                    
                elif self.cost == 'frequency':
                    # cheapest frequency cost is 1 move
                    heuristic += 1
        
        # GPT-5.6 Luna: h0(n) + rarity(goal)
        #if self.cost == 'frequency':
        #   heuristic += dictionary[self.goal]
                    
        return heuristic