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

    ########################################################################################################

class DC(search.Problem):
    """DC is a subclass of the AIMA search files's Problem class. Its init
       method takes three arguments: the initial word, goal word, and cost method.
       A state is represented as a lowercase string of three or four
       ascii characters.  Both the initial and goal states must be
       words of the same length and they must be in the dict
       dictionary. The cost argument specifies how to measure the
       cost of an action and can be 'steps', 'scrabble' or 'frequency'
       """

    ########################################################################################################

    def __init__(self, initial='dog', goal='cat', cost='steps'):
        #TODO: complete this
        # set instance attributes ...
        self.initial = initial
        self.goal = goal
        self.cost = cost
        # make sure arguments are legal, raising an error if any are bad.
        if not initial.islower() or not goal.islower():
            raise Exception("Initial word an Goal word must be lowercase!!")

        if (len(initial) > 4 or len(initial) < 3) or (len(goal) > 4 or len(goal) < 3):
            raise Exception("Initial word and Goal word must have a length of 3 or 4!!")

        if len(initial) != len(goal):
            raise Exception("Length of Initial and Goal must be the same!!")

        if (not goal in dictionary) or (not initial in dictionary):
            raise Exception("Initial and Goal must both be within the dictionary!!")

        if (not cost == 'steps') and (not cost == 'scrabble') and (not cost == 'frequency'):
            raise Exception("Cost must be a supported value: \"steps\", \"scrabble\", or \"frequency\"")



    ########################################################################################################

    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        #list of lists to store all answers
        validActions = []

        #loop through each letter in state then loop through alphabet for each letter in state
        for i in range(len(state)):
            for letter in 'abcdefghijklmnopqrstuvwxyz':

                #create the new word
    #state[:i] = all letters up until letter replaced ... ex/ state = 'cat' & i = 0 --> state[:i] = "" --> i = 2 --> state[:i] = "ca"
    #state[i+1:] = all letters after letter replaced... ex/ state = 'cat' & i = 1 --> state[i+1:] = "t" --> i = 0, state = "at"
                new_word = state[:i] + letter + state[i+1:]

                #if new word is not itself and is a valid new word, add to list
                if (new_word in dictionary) and (not new_word == state):
                    #append(index, letter)
                    validActions.append((i, letter))
        #end function
        return validActions
    
    ########################################################################################################

    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        #we are using the same concept as we did for actions function for appending characters to the string
        #letter to append is stored in action which is a tuple or list or something
        return state[:action[0]] + action[1] + state[action[0]+1:]

    ########################################################################################################

    def goal_test(self, state):
        #TODO: complete this
        """ returns True iff state is a goal state for this problem instance """
        #returns true/false depending if the strings are equal
        return self.goal == state

    ########################################################################################################

    def path_cost(self, c, state1, action, state2):
        #TODO: complete this
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """

        #Answer depends on type of cost metric
        if self.cost == 'steps':
            return c + 1

        if self.cost == 'scrabble':
            ones = ['a', 'e', 'i', 'o', 'u', 'l', 'n', 's', 't', 'r']
            twos = ['d', 'g']
            threes = ['b', 'c', 'm', 'p']
            fours = ['f', 'h', 'v', 'w', 'y']
            fives = ['k']
            eights = ['j', 'x']
            tens = ['q', 'z']

            if action[1] in ones:
                return c + 1
            if action[1] in twos:
                return c + 2
            if action[1] in threes:
                return c + 3
            if action[1] in fours:
                return c + 4
            if action[1] in fives:
                return c + 5
            if action[1] in eights:
                return c + 8
            if action[1] in tens:
                return c + 10

        #by here it must be the frequency metric
        #print(dictionary['cat']) --> Tested and ran this line, it prints the frequency number
        return c + 1 + dictionary[state2]

    ########################################################################################################

    def __repr__(self):
        #TODO: complete this
        """" return a suitable string to represent this problem instance """
        return f"Initial Word: {self.initial}       Goal Word: {self.goal}       Cost Measure: {self.cost}\t"

    ########################################################################################################

    def h(self, node):
        #TODO: complete this
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        #we need a heuristic for each cost type: steps, scrabble and frequency

        #Steps: The number of letters that are different
        if self.cost == 'steps':
            wrongLetters = 0
            for i in range(len(node.state)):
                if node.state[i] != self.goal[i]:
                    wrongLetters += 1
            return wrongLetters

        #Scramble: The letters that are different and their corrseponding value (1, 2, 4, 8, 10, etc...)
        if self.cost == 'scramble':
            ones = ['a', 'e', 'i', 'o', 'u', 'l', 'n', 's', 't', 'r']
            twos = ['d', 'g']
            threes = ['b', 'c', 'm', 'p']
            fours = ['f', 'h', 'v', 'w', 'y']
            fives = ['k']
            eights = ['j', 'x']
            tens = ['q', 'z']

            totalCost = 0
            for i in range(len(node.state)):
                if node.state[i] != self.goal[i]:
                    if self.goal[i] in ones:
                       totalCost += 1
                    if self.goal[i] in twos:
                        totalCost += 2
                    if self.goal[i] in threes:
                        totalCost += 3
                    if self.goal[i] in fours:
                        totalCost += 4
                    if self.goal[i] in fives:
                        totalCost += 5
                    if self.goal[i] in eights:
                        totalCost += 8
                    if self.goal[i] in tens:
                        totalCost += 10
            return totalCost

        #Frequency: The number of different letters times 1 + the smalletst frequency value.
        #if we get here, it must be a frequency cost
        
        #calculating the smallest value in the dictionary
        smallestValue = min(dictionary.values())

        #calc number of wrong letters
        wrongLetters = 0
        for i in range(len(node.state)):
            if node.state[i] != self.goal[i]:
                wrongLetters += 1

        return wrongLetters * (1 + smallestValue)

    ########################################################################################################