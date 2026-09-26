""" starter file for pa1: dogcat """

import search       # AIMA module for search problems
import gzip         # read from a gzip'd file
import sys

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
        self.initial = initial
        self.goal = goal
        self.cost = cost
        # make sure arguments are legal, raising an error if any are bad.
        if len(initial) != len(goal) or len(initial) < 3 or len(initial) > 4:
            print("Length of words arn't valid")
            sys.exit(1)

        if not initial.islower() or not goal.islower():
            print("Words must be lowercase")
            sys.exit(1)

        if initial not in dictionary or goal not in dictionary:
            print("A word is not in the dictionary")
            sys.exit(1)

        if cost not in ('steps', 'scrabble', 'frequency'):
            print("Invalid cost")
            sys.exit(1)

        

    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        #list to return
        actions = []

        for i in range(len(state)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                #dont include the same letter
                if c == state[i]:
                    continue
                word = state[:i] + c + state[i+1:]
                if word in dictionary:
                    actions.append((i,c))
        return actions


    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        word = state[:action[0]] + action[1] + state[action[0]+1:]
        return word

    def goal_test(self, state):
        #TODO: complete this
        """ returns True iff state is a goal state for this problem instance """
        if state == self.goal:
            return True
        else:
            return False

    def path_cost(self, c, state1, action, state2):
        #TODO: complete this
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """

        #cost to add
        cost = 0

        #all actions cost 1
        if self.cost == 'steps':
            return c + 1

        if self.cost == 'scrabble':
            #assigns value to cost based on the letter being changed
            if action[1] in 'aeioulnstr':
                cost = 1
            if action[1] in 'dg':
                cost = 2
            if action[1] in 'bcmp':
                cost = 3
            if action[1] in 'fhvwy':
                cost = 4
            if action[1] in 'k':
                cost = 5
            if action[1] in 'jx':
                cost = 6
            if action[1] in 'qz':
                cost = 10
            
            return c + cost

        if self.cost == 'frequency':
            cost = dictionary[state2] + 1
            return c + cost

    def __repr__(self):
        #TODO: complete this
        """" return a suitable string to represent this problem instance """
        return f"dc({self.initial}, {self.goal}, {self.cost})"

    def h(self, node):
        #TODO: complete this
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        #variable to hold heuristic value
        cost = 0

        #steps heuristic
        if self.cost == 'steps':
            for i in range(len(node.state)):
                if node.state[i] != self.goal[i]:
                    cost += 1
            return cost

        #scrabble heurisitc
        if self.cost == 'scrabble':
            for i in range(len(node.state)):
                if node.state[i] != self.goal[i]:
                    #assigns value to cost based on the letter being changed
                                if self.goal[i] in 'aeioulnstr':
                                    cost += 1
                                if self.goal[i] in 'dg':
                                    cost += 2
                                if self.goal[i] in 'bcmp':
                                    cost += 3
                                if self.goal[i] in 'fhvwy':
                                    cost += 4
                                if self.goal[i] in 'k':
                                    cost += 5
                                if self.goal[i] in 'jx':
                                    cost += 6
                                if self.goal[i] in 'qz':
                                    cost += 10
            return cost

        #frequency heuristic
        if self.cost == 'frequency':
            cost += dictionary[node.state] + 1
            return cost

