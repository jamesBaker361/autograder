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
        self.initial = initial
        self.goal= goal
        self.cost= cost
        # make sure arguments are legal, raising an error if any are bad.
        if (isinstance(self.initial, str) == False or isinstance(self.goal, str) == False):
            raise ValueError("Initial and goal must be strings")
        initial_len= len(self.initial)
        goal_len= len(self.goal)
        if (self.goal != self.goal.lower() or self.initial != self.initial.lower()):
            raise ValueError("Initial and goal words must be lowercase")
        if (goal_len != 3 and goal_len != 4) or (initial_len != 3 and initial_len != 4):
            raise ValueError("Initial and goal words must be 3 or 4 characters long")
        if initial_len != goal_len:
            raise ValueError("Initial and goal words aren't the same length")
        if (self.initial not in dictionary or self.goal not in dictionary):
            raise ValueError("Initial and goal words must be in the dictionary")
        if (self.cost.lower() not in ['steps', 'scrabble', 'frequency']):
            raise ValueError("Cost must be 'steps', 'scrabble', or 'frequency'")

    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """
        action_list= []
        for i, s in enumerate(state):
            for l in range(97,123):
                action = state[0:i] + chr(l) + state[i+1:]
                if (action in dictionary) and (action != state):
                    action_list.append((i, chr(l)))
        return action_list


    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        i, char = action
        return (state[0:i] + char + state[i+1:])

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
        i,char= action
        if self.cost == 'steps':
            return c + 1
        elif self.cost == 'scrabble':
            return c + self.scrabble_value(char)
        elif self.cost == 'frequency':
            return c + 1 + dictionary[state2]
        else:
            return c

    def __repr__(self):
        #TODO: complete this
        """" return a suitable string to represent this problem instance """
        return ('dc(' + self.initial + ', ' + self.goal + ', ' + self.cost + ')')

    def h(self, node):
        #TODO: complete this
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        difference = self.difference(node.state)
        if self.cost == 'steps':
            return len(difference)
        elif self.cost == 'scrabble':
            estimate = 0
            for char in difference:
                estimate += self.scrabble_value(char)
            return estimate
        elif self.cost == 'frequency':
            return len(difference)
        else:
            return len(difference)

    
    # Auxillary function
    def scrabble_value(self, char):
        if char in "aeioulnstr":
            return 1
        elif char in "dg":
            return 2
        elif char in "bcmp":
            return 3
        elif char in "fhwvy":
            return 4
        elif char in "k":
            return 5
        elif char in "jx":
            return 6
        elif char in "qz":
            return 10
        else:
            return 0
        
    def difference(self, node):
        char_difference = []
        for i, c in enumerate(node):
            if c != self.goal[i]:
                char_difference.append(self.goal[i])
        return char_difference

    # Claude
    def h_goal_rarity(self, node):
        h0 = sum(
            1 for i, c in enumerate(node.state)
            if c != self.goal[i]
        )
        
        if h0 == 0:
            return 0

        r_goal = dictionary[self.goal]

        r_min = min(
            rarity
            for word, rarity in dictionary.items()
            if len(word) == len(self.goal)
        )

        return h0 + r_goal + (h0 - 1) * r_min