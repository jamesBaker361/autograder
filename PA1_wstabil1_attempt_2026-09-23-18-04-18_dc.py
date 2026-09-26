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
        if initial not in dictionary.keys():
            raise TypeError("Initial state is not in dictionary")
        if goal not in dictionary.keys():
            raise TypeError("Goal state is not in dictionary")
        if len(initial) != len(goal):
            raise TypeError("Initial and goal states are not words of the same length")
        if cost not in ('steps', 'scrabble', 'frequency', 'ai'):
            raise TypeError("Invalid cost function")

        self.initial = initial
        self.goal = goal
        self.cost = cost


    def actions(self, state):
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """
        actions = []
        for word in dictionary:
            if len(state) == len(word) and state != word:
                action = None
                valid_action = True
                for i, char in enumerate(word):
                    if char != state[i]:
                        if action == None:
                            action = (i, char)
                        else:
                            valid_action = False
                            break
                if valid_action:
                    actions.append(action)

        return actions



    def result(self, state, action):
        """ takes a state and an action and returns a new state """
        return state[:action[0]] + action[1] + state[action[0] + 1:]

    def goal_test(self, state):
        """ returns True iff state is a goal state for this problem instance """
        return (state == self.goal)

    def path_cost(self, c, state1, action, state2):
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """
        if self.cost == 'steps':
            return c + 1
        if self.cost == 'scrabble':
            if action[1] in ('a', 'e', 'i', 'o', 'u', 'l', 'n', 's', 't', 'r'):
                return c + 1
            if action[1] in ('d', 'g'):
                return c + 2
            if action[1] in ('b', 'c', 'm', 'p'):
                return c + 3
            if action[1] in ('f', 'h', 'v', 'w', 'y'):
                return c + 4
            if action[1] == 'k':
                return c + 5
            if action[1] in ('j', 'x'):
                return c + 6
            if action[1] in ('q', 'z'):
                return c + 10
        if self.cost == 'frequency' or self.cost == 'ai':
            return (c + 1 + dictionary[state2])




    def __repr__(self):
        """" return a suitable string to represent this problem instance """
        return f'Initial Word: {self.initial}\nGoal Word: {self.goal}\nCost Measure:{self.cost}\n'

    def h(self, node):
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        if self.cost == 'steps':
            return sum(c1 != c2 for c1, c2 in zip(node.state, self.goal))
        if self.cost == 'scrabble':
            huer = 0
            for c1, c2 in zip(node.state, self.goal):
                if c1 != c2:
                    if c2 in ('a', 'e', 'i', 'o', 'u', 'l', 'n', 's', 't', 'r'):
                        huer += 1
                    elif c2 in ('d', 'g'):
                        huer += 2
                    elif c2 in ('b', 'c', 'm', 'p'):
                        huer += 3
                    elif c2 in ('f', 'h', 'v', 'w', 'y'):
                        huer += 4
                    elif c2 == 'k':
                        huer += 5
                    elif c2 in ('j', 'x'):
                        huer += 6
                    elif c2 in ('q', 'z'):
                        huer += 10
            return huer
        if self.cost == 'frequency':
           if node.state == self.goal:
               return 0
           return (sum(c1 != c2 for c1, c2 in zip(node.state, self.goal)) + dictionary[self.goal])

        # used to test the ai-generated heuristic
        if self.cost == 'ai':
            if node.state == self.goal:
                return 0

            d = sum(c1 != c2 for c1, c2 in zip(node.state, self.goal))

            sorted_rarities = sorted(dictionary.values())
            min_rarity_sum = sum(sorted_rarities[:d])
            
            return d + min_rarity_sum
                
