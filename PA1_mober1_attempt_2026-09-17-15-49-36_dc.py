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

        if not initial.islower():
            raise ValueError("Initial word must be lowercase")
        if not goal.islower():
            raise ValueError("Goal word must be lowercase")
        if len(initial) != len(goal):
            raise ValueError("Initial and goal words must be the same length")
        if len(initial) not in [3, 4]:
                    raise ValueError("Initial and goal words must be the same length")
        if initial not in dictionary or goal not in dictionary:
            raise ValueError("Initial and goal words must be in the dictionary")
        if cost not in ['steps', 'scrabble', 'frequency']:
            raise ValueError("Cost must be 'steps', 'scrabble' or 'frequency'")

        self.initial = initial.lower()
        self.goal = goal.lower()
        self.cost = cost.lower()


        

    def actions(self, state):
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        frontier = []
        if len(state) == 3:
             for i in range(3):
                for char in 'abcdefghijklmnopqrstuvwxyz':
                    new_word = state[:i] + char + state[i+1:]
                    if new_word in dictionary and new_word != state:
                        frontier.append(new_word)
        elif len(state) == 4:
            for i in range(4):
                for char in 'abcdefghijklmnopqrstuvwxyz':
                    new_word = state[:i] + char + state[i+1:]
                    if new_word in dictionary and new_word != state:
                        frontier.append(new_word)
        else:
            raise ValueError("State must be a 3 or 4 letter word")

        return frontier
        

    def result(self, state, action):
        """ takes a state and an action and returns a new state """

        new_state = action
        return new_state


    def goal_test(self, state):
        """ returns True iff state is a goal state for this problem instance """

        if state == self.goal:
            return True
        return False

    def path_cost(self, c, state1, action, state2):
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """

        if self.cost == "steps":
            return c + 1
        elif self.cost == "scrabble":
            scrabble_values = {
                'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1,
                'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 6,
                'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1,
                'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1,
                'u': 1, 'v': 4, 'w': 4, 'x': 6, 'y': 4,
                'z': 10
            }
            for i in range(len(state1)):
                if state1[i] != state2[i]:
                    cost = scrabble_values[state2[i]]
            return c + cost
        elif self.cost == "frequency":
            return c + 1 + dictionary[state2]
        else:
            raise ValueError("Invalid cost metric")

    def __repr__(self):
        """" return a suitable string to represent this problem instance """
        return "dc(initial='%s', goal='%s', cost='%s')" % (self.initial, self.goal, self.cost)

    def h(self, node):
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        cost = 0

        if node.state == self.goal:
            return 0
        elif self.cost == "steps":
            
            if len(node.state) != len(self.goal) or len(node.state) != len(self.initial) or len(node.state) not in [3, 4]:
                raise ValueError("State and goal must be the same length of either 3 or 4 letters")
            else:
                for i in range(len(node.state)):
                    if node.state[i] != self.goal[i]:
                        cost += 1
                return cost 
        elif self.cost == "scrabble":
            if len(node.state) != len(self.goal) or len(node.state) != len(self.initial) or len(node.state) not in [3, 4]:
                raise ValueError("State and goal must be the same length of either 3 or 4 letters")
            scrabble_values = {
                            'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1,
                            'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 6,
                            'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1,
                            'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1,
                            'u': 1, 'v': 4, 'w': 4, 'x': 6, 'y': 4,
                            'z': 10
                        }
            for i in range(len(node.state)):
                if node.state[i] != self.goal[i]:
                    cost += scrabble_values[self.goal[i]]
            return cost
        elif self.cost == "frequency":
            if len(node.state) != len(self.goal) or len(node.state) != len(self.initial) or len(node.state) not in [3, 4]:
                raise ValueError("State and goal must be the same length of either 3 or 4 letters")
            for i in range(len(node.state)):
                                if node.state[i] != self.goal[i]:
                                    cost += 1
            return cost + dictionary[self.goal]
        else:
            raise ValueError("Invalid cost metric")