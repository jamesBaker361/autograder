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

scrabble_groups = [
    ("aeioulnstr", 1),
    ("dg", 2),
    ("bcmp", 3),
    ("fhvwy", 4),
    ("k", 5),
    ("jx", 6),
    ("qz", 10),
]

scrabble_points = {}
for letters, points in scrabble_groups:
    for letter in letters:
        scrabble_points[letter] = points

min_rarity = min(dictionary.values())

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
        self.initial = initial
        self.goal = goal
        self.cost = cost

        # make sure arguments are legal, raising an error if any are bad.
        if not isinstance(initial, str) or not initial.islower():
            raise ValueError(f"initial word must be a lowercase string: {initial!r}")
        if len(initial) not in (3, 4):
            raise ValueError(f"initial word must be 3 or 4 characters long: {initial!r}")

        if not isinstance(goal, str) or not goal.islower():
            raise ValueError(f"goal word must be a lowercase string: {goal!r}")
        if len(goal) not in (3, 4):
            raise ValueError(f"goal word must be 3 or 4 characters long: {goal!r}")

        if len(initial) != len(goal):
            raise ValueError(f"both initial and goal words must be the same length: len({initial!r}) != len({goal!r})")

        if initial not in dictionary or goal not in dictionary:
            raise ValueError("both initial and goal words must be present in the dictionary")

        if not isinstance(cost, str) or cost not in ('steps', 'scrabble', 'frequency'):
            raise ValueError(f"cost must be 'steps', 'scrabble', 'frequency': {cost!r}")

    def actions(self, state):
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """
        legal = []
        for i in range(len(state)):
            for letter in 'abcdefghijklmnopqrstuvwxyz':
                if state[i] == letter:
                    continue
                new_word = state[:i] + letter + state[i+1:]
                if new_word in dictionary:
                    legal.append((i, letter))
        return legal

    def result(self, state, action):
        """ takes a state and an action and returns a new state """
        i, letter = action
        return state[:i] + letter + state[i+1:]

    def goal_test(self, state):
        """ returns True iff state is a goal state for this problem instance """
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """
        if self.cost == 'steps':
            return c + 1
        elif self.cost == 'scrabble':
            return c + scrabble_points[action[1]]
        elif self.cost == 'frequency':
            return c + 1 + dictionary[state2]
        

    def __repr__(self):
        """" return a suitable string to represent this problem instance """
        return f"dc({self.initial}, {self.goal}, {self.cost})"

    def h(self, node):
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        state = node.state
        diff = [i for i in range(len(state)) if state[i] != self.goal[i]]
        if not diff:
            return 0

        if self.cost == 'steps':
            return len(diff)
        elif self.cost == 'scrabble':
            return sum(scrabble_points[self.goal[i]] for i in diff)
        elif self.cost == 'frequency':
            return (1 + dictionary[self.goal]) + (len(diff) - 1) * (1 + min_rarity)

