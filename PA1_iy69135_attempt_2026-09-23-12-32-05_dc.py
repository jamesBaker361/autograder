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
    """
    DC is a subclass of the AIMA search files's Problem class. Its init
    method takes three arguments: the initial word, goal word, and cost method.

    A state is represented as a lowercase string of three or four
    ascii characters.  Both the initial and goal states must be
    words of the same length and they must be in the dict
    dictionary. 
    
    The cost argument specifies how to measure the
    cost of an action and can be 'steps', 'scrabble' or 'frequency'
    """


    def __init__(self, initial='dog', goal='cat', cost='steps'):
        #TODO: complete this
        # set instance attributes ...
        # populate initialized variables with values given via command-line arguments
        self.initial = initial
        self.goal = goal
        self.cost = cost

        # make sure arguments are legal, raising an error if any are bad.
        # validate if the initial word is contained in the word dictionary
        if initial not in dictionary:
            raise ValueError("Initial word is not in dictionary")

        # validate if the goal word is contained in the word dictionary
        if goal not in dictionary:
            raise ValueError("Goal word is not in dictionary")

        # validate that the initial and goal words are the same length
        if len(initial) != len(goal):
            raise ValueError("Arguments consist of different sizes")

        # ensure cost is populated
        if cost not in ['steps', 'scrabble', 'frequency']:
            raise ValueError("Invalid cost method")


    def actions(self, state):
        #TODO: complete this
        """ 
        Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  
        
        An action is defined by position in the word and a character to
        put in that position.  But the result must be a legal word, i.e.,
        in our dictionary, and it should not be the same as the state, 
        i.e., don't replace a character with the same character 
        """

        # array that stores all possible actions for the current state
        actions = []

        # string storing all characters in the alphabet so that they can be checked with each index of the current state string
        alphabet = 'abcdefghijklmnopqrstuvwxyz'

        # iterate through each character position in the current word
        for i in range(len(state)):
            # iterate through each letter of the alphabet
            for letter in alphabet:
                # skip the iteration if the state is evaluating it's current letter at any string index
                # prevents same-character replacement on any index of the state string
                if letter == state[i]:
                    continue

                # create an action by slicing the i'th element of the current word and replacing it with the current letter
                # any indices in the state string that are not the i'th element stay the same
                new_word = state[:i] + letter + state[i + 1:]

                # append the new state into the actions array, if the word is deemed valid by the dicitoonary array
                if new_word in dictionary:
                    actions.append((i, letter))

        # return entire array of actions once the outer-loop terminates
        return actions
        

    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        position, letter = action
        return state[:position] + letter + state[position + 1:]


    def goal_test(self, state):
        #TODO: complete this
        """ returns True iff state is a goal state for this problem instance """
        # check if the current state matches the goal state and rtuen true; retunr false otherwise
        if state == self.goal:
            return True
        else:
            return False
        

    def path_cost(self, c, state1, action, state2):
        #TODO: complete this
        """ 
        Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. 
        
        For the the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency 
        """

        # initiaize the scabble path cost for each letter
        scrabble_values = {
            'a':1, 'e':1, 'i':1, 'o':1, 'u':1, "l":1, 'n':1, 's':1, 't':1, 'r':1,
            'd':2, 'g':2,
            'b':3, 'c':3, 'm':3, 'p':3,
            'f':4, 'h':4, 'v':4, 'w':4, 'y':4,
            'k':5,
            'j':6, 'x':6,
            'q':10, 'z':10
        }

        if self.cost == 'steps':
            return c + 1
        
        # applies the cost of a letter given the action
        elif self.cost == 'scrabble':
            position, letter = action
            return c + scrabble_values[letter]

        # scans the dicitonary for the rarity of state2
        elif self.cost == 'frequency':
            return c + 1 + dictionary[state2]


    def __repr__(self):
        #TODO: complete this
        """ return a suitable string to represent this problem instance """
        return f"dc({self.initial}, {self.goal}, {self.cost})"


    def h(self, node):
        #TODO: complete this
        """
        Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. 
        
        The heuristic's value should depend on the Problem's cost parameter,
        self.cost (i.e., steps, scrabble or frequency), as this will effect 
        the estimate cost to get to the nearest goal.
        """
        # get the current state
        state = node.state

        # gather the heuristic based on the cost parameter
        # the steps and frequency cost parameters utilize the same heuristic
        if self.cost == 'steps' or self.cost == 'frequency':
            # track the differences from the current state from the goal state
            differences = 0

            # increment differences for each letter in the current state that contains a descrepency
            for i in range(len(state)):
                if state[i] != self.goal[i]:
                    differences += 1

            # return the number of differences
            return differences

        #################################################################################################################
        # The following conditional code is generated by ChatGPT 5.6 Luna
        # question 4 requires us to ask a given prompt into an LLM and verify it's given heuristic. I have asked
        # the model to generate code for its own heuristic, which will be tested alongside my own implementation.
        # Comments were provided by myself to help understand the implementation. Upon testing, one of the 
        # implementations is commented out so the other can run.
        
        # # gather the heuristic based on the cost parameter
        # # the steps and frequency cost parameters utilize the same heuristic
        # if self.cost == 'steps' or self.cost == 'frequency':
        #     # track the differences from the current state from the goal state
        #     differences = 0

        #     # increment differences for each letter in the current state that contains a discrepancy
        #     for i in range(len(state)):
        #         if state[i] != self.goal[i]:
        #             differences += 1

        #     # if we are already at the goal, the remaining cost is 0
        #     if differences == 0:
        #         return 0

        #     # find the minimum rarity among all non-goal dictionary words
        #     min_rarity = float('inf')

        #     # iterate each potential next state in the dictionary
        #     for word in dictionary:
        #         if word != self.goal:
        #             if dictionary[word] < min_rarity:
        #                 min_rarity = dictionary[word]

        #     # get the rarity of the goal word
        #     goal_rarity = dictionary[self.goal]

        #     # uses the provided equation to determine the heuristic, which is then returned
        #     heuristic = (
        #         differences
        #         + (differences - 1) * min_rarity
        #         + goal_rarity
        #     )

        #     return heuristic

        # END OF GENERATED CODE
        #################################################################################################################


        elif self.cost == "scrabble":
            # gstores the heuristic cost
            cost = 0

            # initiaize the scabble heutristic cost for each letter
            scrabble_values = {
                'a':1, 'e':1, 'i':1, 'o':1, 'u':1, "l":1, 'n':1, 's':1, 't':1, 'r':1,
                'd':2, 'g':2,
                'b':3, 'c':3, 'm':3, 'p':3,
                'f':4, 'h':4, 'v':4, 'w':4, 'y':4,
                'k':5,
                'j':6, 'x':6,
                'q':10, 'z':10
            }

            """
            The only thing the algorithm knows for sure is that it must, at some point,
            reach the goal state. Therefore, a valid heuristic is taking the scrabble cost
            of each letter of the goal state, only disqualifying the index if the current 
            state matches the goal state, as that letter index no longer needs to be modified
            """
            # iterate through each index in the current state string
            for i in range(len(state)):
                # compare the current word state index to the goal state index
                if state[i] != self.goal[i]:
                    # if the match is not made, add to the cost the scrabble value of the goal state word at the i'th index
                    cost += scrabble_values[self.goal[i]]

            # return the heuristic
            return cost
