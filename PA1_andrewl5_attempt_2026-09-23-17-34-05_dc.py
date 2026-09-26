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

        alphabet_list = ['a', 'b', 'c', 'd', 'e', 'f',
                         'g', 'h', 'i', 'j', 'k', 'l',
                         'm', 'n', 'o', 'p', 'q', 'r',
                         's', 't', 'u', 'v', 'w', 'x',
                         'y', 'z']
        valid_list = []

        for i in range(len(state)):
            for j in range(len(alphabet_list)):
                word_copy = state
                word_copy = list(word_copy)
                word_copy[i] = alphabet_list[j]
                word_copy = "".join(word_copy)
                if ((state[i] != alphabet_list[j]) and (word_copy in dictionary)):
                    valid_list.append([i, alphabet_list[j]])
        return valid_list


    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        word_copy = list(state)
        word_copy[action[0]] = action[1]
        word_copy = "".join(word_copy)
        return word_copy

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

        letter_cost = {
            'a': 1,
            'e': 1,
            'i': 1,
            'o': 1,
            'u': 1,
            'l': 1,
            'n': 1,
            's': 1,
            't': 1,
            'r': 1,
            'd': 2,
            'g': 2,
            'b': 3,
            'c': 3,
            'm': 3,
            'p': 3,
            'f': 4,
            'h': 4,
            'v': 4,
            'w': 4,
            'y': 4,
            'k': 5,
            'j': 6,
            'x': 6,
            'q': 10,
            'z': 10
        }

        if (self.cost == 'steps'):
            return c + 1
        elif (self.cost == 'scrabble'):
            for i in range(len(state1)):
                if (state1[i] != state2[i]):
                    return c + letter_cost[state2[i]]

        elif (self.cost == 'frequency'):
            return c + (1 + dictionary[state2])
        return c + 1
                

    def __repr__(self):
        #TODO: complete this
        """" return a suitable string to represent this problem instance """
        return 'DOGCAT(initial=' + self.initial + ', goal=' + self.goal + ', cost=' + self.cost + ')'

    def h(self, node):
        #TODO: complete this
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        """
        A admissible heuristic:
            -- h(n) for every node has to be <= h*(n)
            -- h(n) ≤ c(n, n') + h(n') or h(A) - h(C) <= cost(A to C)

        hmmmm perhaps 
        -- just simply letter difference count
        -- for each letter in the word, calculate letter distance?
            -- but would I need to assume that the alphabet loops around? or just count the letter values one way?
        -- count number of letters different by position?

        Testing:
        DOG -> CAT (steps)
        DOG -> COG -> COT -> CAT
        g(n) = 3
        h(DOG) = 3
        h(COG) = 2
        h(CAG) = 1
        h(CAT = 0)
        Seems to work

        DOG -> CAT (scrabble)
        DOG -> COG -> COT -> CAT
        Calculate what letters are still missing and it's total cost
        g(n) = 5
        h(DOG) = 5
        h(COG) = 2
        h(COT) = 1
        h(CAT) = 0
        seems to work?

        DOG -> CAT (rarity)
        DOG -> COG -> COT -> CAT
        Calculate how many letters are missing and multiple it by the current word's rarity value.
        g(n) = 34.171195
        h(DOG) = 3
        h(COG) = 2
        h(COT) = 1
        h(CAT) = 0
        seems to work?
        """
        letter_cost = {
            'a': 1,
            'e': 1,
            'i': 1,
            'o': 1,
            'u': 1,
            'l': 1,
            'n': 1,
            's': 1,
            't': 1,
            'r': 1,
            'd': 2,
            'g': 2,
            'b': 3,
            'c': 3,
            'm': 3,
            'p': 3,
            'f': 4,
            'h': 4,
            'v': 4,
            'w': 4,
            'y': 4,
            'k': 5,
            'j': 6,
            'x': 6,
            'q': 10,
            'z': 10
        }

        if (self.cost == "steps"):
            difference_count = 0
            for i in range(len(node.state)):
                if (node.state[i] != self.goal[i]):
                    difference_count += 1
            return difference_count
        elif (self.cost == "scrabble"):
            total_cost_difference = 0
            for i in range(len(node.state)):
                if (node.state[i] != self.goal[i]):
                    total_cost_difference += letter_cost[self.goal[i]]
            return total_cost_difference
        elif (self.cost == "frequency"):
            difference_count = 0
            for i in range(len(node.state)):
                if (node.state[i] != self.goal[i]):
                    difference_count += 1
            total_cost_difference = (difference_count * dictionary['the']) + difference_count
            # Below is the AI proposed heuristic
            # estimated_cost = (1 + dictionary['the']) * (difference_count - 1) + (1 + dictionary[self.goal])
            return total_cost_difference
        return 1
