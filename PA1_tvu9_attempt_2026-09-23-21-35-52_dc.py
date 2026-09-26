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

scrabble_value = {
    'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1,'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
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
        # set instance attributes ...

        # both initial and goal input have to be strings
        if not isinstance(initial, str) or not isinstance(goal, str):
            raise ValueError("Initial and goal have to both be strings")

        # words for initial and goal have to be in the dictionary
        if initial not in dictionary or goal not in dictionary:
            raise ValueError("Words for initial and goal have to be in the dictionary")

        # words have to be three or four letters
        if len(initial) not in (3,4) or len(goal) not in (3,4):
            raise ValueError("Words for initial and goal have to be three or four letters")

        # words have to be lowercase
        if not initial.islower() or not goal.islower():
            raise ValueError("Words must all be lowercase")

        # both initial and goal have to be same length
        if len(initial) != len(goal):
            raise ValueError("Both initial and goal have to be same length in letters")

        # check for valid cost method
        if cost not in ('steps', 'frequency', 'scrabble'):
            raise ValueError("Not a valid cost")

        # we initialize the AIMA problem class to store initial and goal
        super().__init__(initial, goal)

        # store cost method since the constructor in the AIMA problem class doesn't
        self.cost = cost
        
    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        available_actions = []

        for position in range(len(state)):
            for letter in alphabet:

                # checks if the letter is itself
                if letter == state[position]:
                    continue

                # creates new possible word
                word = (state[:position] + letter + state[position + 1:])

                # check if the new possible word exist in the dictionary
                if word in dictionary:
                    available_actions.append((position, letter))

        # return all available actions
        return available_actions
        

    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """

        # unpack the tuple
        position, letter = action

        # replace letter
        state = (state[:position] + letter + state[position + 1:])

        # return new state after performing a step
        return state
        
    def goal_test(self, state):
        #TODO: complete this
        """ returns True iff state is a goal state for this problem instance """
        # return true if the state equals to the goal
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        #TODO: complete this
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """
        
        
        if self.cost == 'steps':
            # always adds 1 to the cost 
            return c + 1
        
        elif self.cost == 'scrabble':
            letter = action[1]
            # add given value assigned to respective letter based on the letter of the next available action
            return c + scrabble_value[letter]
        
        elif self.cost == 'frequency':
            # we want to add the rarity of the next state instead of the initial state before and adding 1 from the formula [1 + rarity(w)]
            return c + dictionary[state2] + 1
        

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

        state = node.state

        # we want to find mismatches of every letter from the initial to the goal to determine how many replacements are unavoidable
        number_of_mismatches = sum(
            state[i] != self.goal[i]
            for i in range(len(state))
        )

        if self.cost == 'steps':
            # returns a count of how many positions differ from the goal which can underestimate the actual path cost
            return number_of_mismatches
        
        elif self.cost == 'scrabble':
            estimation = 0
            # we want to add up all the values of letters that will eventually have to be changed for the goal
            for i in range(len(state)):
                if state[i] != self.goal[i]:
                    estimation += scrabble_value[self.goal[i]]

            return estimation

        elif self.cost == 'frequency':
            if state == self.goal:
                return 0
            # we want to return the rarity of the goal word because eventually the initial state will have to enter the goal word. We also know that any other actions cost at least 1 so we count for amount of mismatches that has to be changed to reach the goal. This method highly underestimates the actual cost, but acts as a good lower bound for estimation. 
            return dictionary[self.goal] + number_of_mismatches
