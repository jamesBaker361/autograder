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

        if len(initial) != len(goal):
            raise ValueError("initial and goal must be the same length")
        if cost != "steps" and cost != "scrabble" and cost != "frequency":
            raise ValueError("invalid cost type")

        self.goal = goal
        self.initial = initial
        self.cost = cost


    def actions(self, state):

        # Tuples of (position of changable letter, letter that it can change to)
        actionList = []

        # Loops for every letter for current state (3 or 4)
        for i in range(len(state)):
            for j in 'abcdefghijklmnopqrstuvwxyz':

                # Does not allow current letter, tries to form word in dict
                if j != state[i]:

                    possibleWord = state[:i] + j + state[1+i:]
                    if possibleWord in dictionary:
                        actionList.append((i,j))

        return actionList

    def result(self, state, action):

        """ takes a state and an action and returns a new state """
        position = action[0]
        newLetter = action[1]
        return state[:position] + newLetter + state[position+1:]

    def goal_test(self, state):

        """ returns True iff state is a goal state for this problem instance """
        return state == self.goal
    
    def path_cost(self, c, state1, action, state2):

        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """

        # Steps cost actions
        if self.cost == "steps":
            return c + 1

        # Scrabble cost actions
        elif self.cost == "scrabble":

            # Groupings of letters for scrabble cost
            replacementMatrix = [
                ["a", "e", "i", "o", "u", "l", "n", "s", "t", "r"],
                ["d", "g"],
                ["b", "c", "m", "p"],
                ["f", "h", "v", "w", "y"],
                ["k"],
                ["j", "x"],
                ["q", "z"]
            ]

            # Corresponding costs to matrix rows
            costVector = [1,2,3,4,5,6,10]

            # Iterates through each row
            for matrixRow in range(len(replacementMatrix)):

                # Iterates through each column
                for matrixColumn in range(len(replacementMatrix[matrixRow])):

                    # If action letter is the same as the one interated...
                    if action[1] == replacementMatrix[matrixRow][matrixColumn]:

                        # Returns the current corresponding cost and cumulative (c)
                        return costVector[matrixRow] + c

        # Scrabble cost frequency
        elif self.cost == "frequency":
            return 1 + dictionary[state2] + c
        

    def __repr__(self):

        """" return a suitable string to represent this problem instance """
        return "dc("+self.initial+ "," + self.goal + "," + self.cost + ")"

    def h(self, node):

        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        heuristic = 0
        if self.cost == "steps" or self.cost == "frequency":

            # Heuristic is how many mismatched letters there are to goal state
            for i in range(len(node.state)):
                if node.state[i] != self.goal[i]:
                    heuristic += 1

        elif self.cost == "scrabble":
            for i in range(len(node.state)):
                if node.state[i] != self.goal[i]:

                    # Heuristic is from the cost vector in cost function
                    heuristic += self.path_cost(0, node.state, (i, self.goal[i]), self.goal)

        return heuristic
