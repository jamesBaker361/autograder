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
        self.initial=initial
        self.goal=goal
        self.cost=cost

        if (not initial.islower() or not goal.islower()
            or len(initial) != len(goal) or len(initial) not in (3, 4)
            or initial not in dictionary or goal not in dictionary or cost not in ('steps', 'scrabble', 'frequency')):
            raise ValueError(f"Bad initial or goal word or cost measure: {initial} {goal} {cost}") 

    def actions(self, state):
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        children = []

        for index in range(len(state)):
            letters = list(state)

            for char in range(ord('a'), ord('z') + 1):
                letters[index] = chr(char)
                word = str.join('', letters)

                if state != word and word in dictionary:
                    children.append((index, chr(char)))

        return children

    def result(self, state, action):
        """ takes a state and an action and returns a new state """
        return f"{state[:action[0]]}{action[1]}{state[action[0] + 1:]}"

    def goal_test(self, state):
        """ returns True if state is a goal state for this problem instance """
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """    

        match self.cost:
            case 'steps':
                return c + 1
            case 'scrabble':
                return c + self.letter_value(action[1])
            case 'frequency':
                return c + 1 + dictionary[state2]

    def __repr__(self):
        """ return a suitable string to represent this problem instance """
        return f"initial: {self.initial}, goal: {self.goal}, cost measure: {self.cost}"

    def h(self, node):
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        letters = [goal_letter
                   for node_letter, goal_letter in zip(node.state, self.goal)
                   if node_letter != goal_letter]

        match self.cost:
            case 'steps':
                return len(letters)
            case 'scrabble':
                return sum(map(self.letter_value, letters))
            case 'frequency':
                if node == self.goal:
                    return 0
                return (1 + dictionary[self.goal]) + (len(letters) - 1) * (1 + self.min_frequency())

    def letter_value(self, char):
        match char:
            case "a" | "e" | "i" | "o" | "u" | "l" | "n" | "s" | "t" | "r":
                return 1
            case "d" | "g":
                return 2
            case "b" | "c" | "m" | "p":
                return 3
            case "f" | "h" | "v" | "w" | "y":
                return 4
            case "k":
                return 5
            case "j" | "x":
                return 6
            case "q" | "z":
                return 10

    def min_frequency(self):
        return min(dictionary.values())