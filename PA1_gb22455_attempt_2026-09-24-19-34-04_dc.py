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

# dictionary for scrabble letter costs
# utilized ChatGPT to create the dictionary 
# using the values in the assignment document
# is double checked to ensure correctness
scrabble_dict = {
    'a': 1,
    'b': 3,
    'c': 3,
    'd': 2,
    'e': 1,
    'f': 4,
    'g': 2,
    'h': 4,
    'i': 1,
    'j': 6,
    'k': 5,
    'l': 1,
    'm': 3,
    'n': 1,
    'o': 1,
    'p': 3,
    'q': 10,
    'r': 1,
    's': 1,
    't': 1,
    'u': 1,
    'v': 4,
    'w': 4,
    'x': 6,
    'y': 4,
    'z': 10
    }

class IllegalWordError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    def __str__(self):
        return f"{self.message}"

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
        if self.initial not in dictionary:
            raise IllegalWordError("Initial word is not in acceptable list!")
        if self.goal not in dictionary:
            raise IllegalWordError("Goal word is not in acceptable list!")
        if self.cost not in {'steps', 'scrabble', 'frequency'}:
            raise IllegalWordError("Cost method is not in acceptable list!")
        if len(self.initial) != len(self.goal):
            raise IllegalWordError("Initial and Goal are not the same length!")


    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """
        actions = []
        for key in dictionary.keys():
            if len(key) != len(state):
                continue

            matching_letter_count = 0

            for i in range(len(state)):
                if key[i] == state[i]:
                    matching_letter_count += 1

            if matching_letter_count == len(state) - 1:
                for i in range(len(key)):
                    if key[i] != state[i]:
                        actions.append((i,key[i]))
                    

        return actions

    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        index, letter = action
        new_state = ""
        for i in range(len(state)):
            if i != index:
                new_state += state[i]
            else:
                new_state += letter

        return new_state




    def goal_test(self, state):
        #TODO: complete this
        """ returns True iff state is a goal state for this problem instance """
        if state == self.goal:
            return True
        return False

    def path_cost(self, c, state1, action, state2):
        #TODO: complete this
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """
        if self.cost == 'steps':
            c += 1
            return c
        elif self.cost == 'scrabble':
            index, letter = action
            return c + scrabble_dict[letter]
        else:
            return c + 1 + dictionary[state2]

    def __repr__(self):
        #TODO: complete this
        """" return a suitable string to represent this problem instance """
        return f"Initial state: {self.initial}\nGoal state: {self.goal}\nCost metric: {self.cost}"

    def h(self, node):
        #TODO: complete this
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        if self.cost == 'steps':
            unmatch_letter_count = 0
            for i in range(len(node.state)):
                if self.goal[i] != node.state[i]:
                    unmatch_letter_count += 1

            return unmatch_letter_count
        
        elif self.cost == 'scrabble':
            unmatch_letter_count = 0
            for i in range(len(node.state)):
                if self.goal[i] != node.state[i]:
                    unmatch_letter_count += 1

            sum_scrabble_cost = 0
            for value in scrabble_dict.values():
                sum_scrabble_cost += value
            average_scrabble_cost = sum_scrabble_cost / len(scrabble_dict)

            return unmatch_letter_count * average_scrabble_cost
        
        else:
            unmatch_letter_count = 0
            for i in range(len(node.state)):
                if self.goal[i] != node.state[i]:
                    unmatch_letter_count += 1

            sum_frequency_cost = 0
            for value in dictionary.values():
                sum_frequency_cost += value
            average_frequency_cost = sum_frequency_cost / len(dictionary)

            return unmatch_letter_count * (1 + average_frequency_cost)
            

