""" starter file for pa1: dogcat """

import search       # AIMA module for search problems
import gzip         # read from a gzip'd file
from string import ascii_lowercase


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
        # checks if strings are lowercase if not then raises an error
        if(goal.lower() != goal or initial.lower() != initial):
            raise ValueError("Words must be lowercase")
        # checks if cost types are valid if not then raises an error
        if(cost != 'steps' and cost != 'scrabble' and cost != 'frequency'):
            raise ValueError("Cost must be steps, scrabble or frequency")
        # checks if initial and goal are teh same length
        if(len(goal) != len(initial)):
            raise ValueError("Words must be the same length")
        # checks if initial and goal are 3 or 4 letters long
        if(len(goal) < 3 or len(goal) > 4):
            raise ValueError("Words must be 3 or 4 letters long")
        # checks if initial and goal are both in the dictionary if not then raises an error
        if(goal not in dictionary or initial not in dictionary):
            raise ValueError("Words must be in the dictionary")



    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """
        alphabet = ascii_lowercase
        possible_actions = []
        # loops through the length of the word and for each letter in the alphabet
        for i in range(len(self.goal)):
            for letter in alphabet:
                # checks if the letter is different from the ith letter in the state
                if letter != state[i]:
                    # replaces the ith letter in the state with the new letter
                    new_word = state[:i] + letter + state[i+1:]
                    # checks if the new word is actually in the dictionary
                    if new_word in dictionary:
                        possible_actions.append((i, letter))
        return possible_actions

    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        # creates a list to replace letter
        state_list = list(state)
        # replaces the  old letter with the new one
        state_list[action[0]] = action[1]
        # turns list back into string
        new_state = "".join(state_list)
        return new_state


    def goal_test(self, state):
        #TODO: complete this
        """ returns True iff state is a goal state for this problem instance """
        if(self.goal == state):
            return True
        return False

    def path_cost(self, c, state1, action, state2):
        #TODO: complete this
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """
        # if the cost is based off steps then 1 is added for each step
        if self.cost == 'steps':
            return c + 1
        # if teh cost is based off scrabble then the cost of the letter is added to the total cost
        elif self.cost == 'scrabble':
            scrabble_values = {
                'a':1, 'e':1, 'i':1, 'o':1, 'u':1, 'l':1, 'n':1, 's':1, 't':1, 'r':1,
                'd':2, 'g':2,'b':3, 'c':3, 'm':3, 'p':3,
                'f':4, 'h':4, 'v':4, 'w':4, 'y':4, 'k':5, 'j':6, 'x':6, 'q':10, 'z':10
            }
            return c + scrabble_values[action[1]]
        # if the cost is based off frequency then 1 is added for each step and the
        # frequency of the new word is added to the total cost
        elif self.cost == 'frequency':
            return c + 1 + dictionary[state2]
        pass

    def __repr__(self):
        #TODO: complete this
        """" return a suitable string to represent this problem instance """
        return f"dc(initial={self.initial}, goal={self.goal}, cost={self.cost})"

    def h(self, node):
        #TODO: complete this
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        heuristic_cost = 0
        # if the goal is reached, return 0
        if(node.state == self.goal):
            return heuristic_cost
        # computes the heuristic cost based on the steps cost metric
        if self.cost == 'steps':
            # loops through length of the word and adds 1 for each letter that is different from the goal word
            for i in range(len(node.state)):
                if node.state[i] != self.goal[i]:
                    heuristic_cost += 1
        # computes the heuristic cost based on the scrabble cost metric
        elif self.cost == 'scrabble':
            # creates a dictionary of scrabble costs for each letter
            scrabble_values = {
                'a':1, 'e':1, 'i':1, 'o':1, 'u':1, 'l':1, 'n':1, 's':1, 't':1, 'r':1,
                'd':2, 'g':2,'b':3, 'c':3, 'm':3, 'p':3,
                'f':4, 'h':4, 'v':4, 'w':4, 'y':4, 'k':5, 'j':6, 'x':6, 'q':10, 'z':10
            }
            # loops through length of the word and adds the cost of teh replacement letter
            # for each letter that is different from the goal word
            for i in range(len(node.state)):
                if node.state[i] != self.goal[i]:
                    heuristic_cost += scrabble_values[self.goal[i]]
        # computes the heuristic cost based on the frequency cost metric
        elif self.cost == 'frequency':
            # loops through length of the word and adds 1 for each letter that is different from the goal word
            for i in range(len(node.state)):
                if node.state[i] != self.goal[i]:
                    heuristic_cost += 1
            # adds the frequency of the goal word to the total heuristic cost
            heuristic_cost += dictionary[self.goal]
        return heuristic_cost
        pass

