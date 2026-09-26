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

def scrabble_cost(letter):
    if letter in "aeioulnstr":
        return 1
    elif letter in "dg":
        return 2
    elif letter in "bcmp":
        return 3
    elif letter in "fhvwy":
        return 4
    elif letter == "k":
        return 5
    elif letter in "jx":
        return 6
    elif letter in "qz":
        return 10

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

        if not initial.islower() or not goal.islower():
            raise ValueError("Words must be lowercase")

        if initial not in dictionary:
            raise ValueError("The initial word does not exist in the dictionary")
        if goal not in dictionary: 
            raise ValueError("Goal word does not exist in dictionry")

        # Check if the lenghts match
        if len(initial) != len(goal):
            raise ValueError("Words must be the same length")
        if len(initial) != 3 and len(initial) != 4:
            raise ValueError("Words must be 3 or 4 letters long")

        # checking valid cost type
        match cost:
            case 'steps':
                pass
            case 'scrabble':
                pass
            case 'frequency':
                pass
            case _:
                raise ValueError("invalid cost method")

    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        actions = []

        for i in range(len(state)):
            for letter in "abcdefghijklmnopqrstuvwxyz":

                #try every lowercase letter from the letter string.
                if letter != state[i]:
                    new_word = state[:i] + letter + state[i + 1:]

                    if new_word in dictionary:
                        actions.append((i,letter))
        return actions


    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        i, letter = action

        new_state = state[:i] + letter + state[i + 1:]

        return new_state

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

        match self.cost:
            case 'steps':
                return c + 1
            case 'scrabble':
                i, letter = action
                return c + scrabble_cost(letter)

            case 'frequency':
                return c + 1 + dictionary[state2]

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
        different = 0

        # count how many letters are different from the goal
        for i in range(len(state)):
            if state[i] != self.goal[i]:
                different += 1

        # heuristic must be reach 0 if the goal is completed
        if different ==  0:
            return 0

        match self.cost:

            case 'steps':
                return different

            case 'scrabble':
                cost = 0

                for i in range(len(state)):
                    if state[i] != self.goal[i]:
                        cost += scrabble_cost(self.goal[i])

                return cost
            case 'frequency':
                return different + dictionary[self.goal]
