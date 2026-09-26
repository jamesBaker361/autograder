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
        # check if input is string
        if not isinstance(initial, str) or not isinstance(goal, str):
            raise ValueError("Initial and goal must be strings")
        # validate lowercase
        if (not initial.islower()) or (not goal.islower()):
            raise ValueError("Error: Initial and goal state strings must be fully lowercase")

        if (len(initial) != 3) and (len(initial) != 4):
            raise ValueError("Error: Error: Initial state string must be three or four letters")
        # validate length
        if (len(goal) != 3) and (len(goal) != 4):
            raise ValueError("Error: Error: Goal state string must be three or four letters")
        if len(initial) != len(goal):
            raise ValueError("Error: Initial and goal state strings must be same length")
        # validate if in dictionary
        if (initial not in dictionary) or (goal not in dictionary):
            raise ValueError("Error: Initial and goal state strings must appear in the dictionary")
        # validate cost 
        if (cost != "steps") and (cost != "scrabble") and (cost != "frequency"):
            raise ValueError ("Error: Cost argument is invalid")
        # make sure arguments are legal, raising an error if any are bad.
        self.initial = initial
        self.goal = goal
        self.cost = cost
        pass

    def actions(self, state):
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """
        actionList = []
        ogState = state
        stateCopy = state
        # iterate over current state
        for i in range(len(state)):
            # iterate over alphabet
            for j in range(ord('a'), ord('z') + 1):
                # test word
                stateCopy = state[:i] + chr(j) + state[i+1:]
                # if swapping the current letter is a valid (and new) word
                if stateCopy in dictionary and stateCopy != ogState:
                    actionList.append((i, chr(j)))
                stateCopy = ogState
        return actionList

    def result(self, state, action):
        """ takes a state and an action and returns a new state """
        index = action[0]
        newLetter = action[1]
        newState = state[:index] + newLetter + state[index+1:]
        return newState

    def goal_test(self, state):
        """ returns True iff state is a goal state for this problem instance """
        if (self.goal == state):
            return True

        return False

    def path_cost(self, c, state1, action, state2):
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """

        if self.cost == "steps":
            c += 1

        elif self.cost == "scrabble":
            newLetter = action[1]

            scrabbleVals = {"a":1, "e":1, "i":1, "o":1, "u":1, "l":1, "n":1, "s":1, "t":1, "r":1,
                            "d":2, "g":2, "b":3, "c":3, "m":3, "p":3, "f":4, "h":4, "v":4, "w":4, "y":4,
                            "k":5, "j":6, "x":6, "q":10, "z":10}
            c += scrabbleVals[newLetter]

        elif self.cost == "frequency":
            c += 1 + dictionary[state2]

        return c

    def __repr__(self):
        """" return a suitable string to represent this problem instance """
        instanceString = f"dc({self.initial},{self.goal},{self.cost})"
        return instanceString

    def h(self, node):
        #TODO: complete this
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        cost = 0
        if self.cost == "steps":
            for i in range(len(self.goal)):
                if self.goal[i] != node.state[i]:
                    cost += 1
            
        elif self.cost == "scrabble":
            scrabbleVals = {"a":1, "e":1, "i":1, "o":1, "u":1, "l":1, "n":1, "s":1, "t":1, "r":1,
                            "d":2, "g":2, "b":3, "c":3, "m":3, "p":3, "f":4, "h":4, "v":4, "w":4, "y":4,
                            "k":5, "j":6, "x":6, "q":10, "z":10}
            for j in range(len(self.goal)):
                if self.goal[j] != node.state[j]:
                    cost += scrabbleVals[self.goal[j]]

        elif self.cost == "frequency":
            for k in range(len(self.goal)):
                if self.goal[k] != node.state[k]:
                    cost += 1

            if cost > 0:
                cost += dictionary[self.goal]

        return cost
