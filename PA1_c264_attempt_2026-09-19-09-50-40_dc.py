""" starter file for pa1: dogcat """
""" 
Author: Charles Dang
Date: September 15th, 2026
Course: CMSC 471, Section 3
"""

import search       # AIMA module for search problems
import gzip         # read from a gzip'd file
import string       # for string.ascii_lowercase

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

# scrabble is a dict mapping lowercase letters to scrabble value,
# used by the 'scrabble' cost measure. 

scrabble = {}
for value, letters in ((1, 'aeioulnstr'), (2, 'dg'), (3, 'bcmp'),
                       (4, 'fhvwy'), (5, 'k'), (6, 'jx'), (10, 'qz')):
    for letter in letters:
        scrabble[letter] = value

# rarity of the most common word in the dictionary. No action can ever
# cost less than 1+min_rarity under the frequency measure, so the frequency
# heuristic uses this as its lower bound on the cost of a single action.

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
        for word, label in ((initial, 'initial'), (goal, 'goal')):
            if not isinstance(word, str):
                raise ValueError(f"{label} word must be string, {word!r}")
            if not (word.isalpha() and word.islower()):
                raise ValueError(f"{label} word not all lowercase, {word!r}")
            if len(word) not in (3, 4):
                raise ValueError(f"{label} word in range [3,4] {word!r}")
            if word not in dictionary:
                raise ValueError(f"{label} word not found in dict {word!r}")
        if len(initial) != len(goal):
            raise ValueError(f"{initial!r} and {goal!r} must be  same length")
        if cost not in ('steps', 'scrabble', 'frequency'):
            raise ValueError(f"cost must be steps, scrabble or frequency, {cost!r}")

        search.Problem.__init__(self, initial, goal)
        self.cost = cost

    def actions(self, state):
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        allowed = []
        for position in range(len(state)):
            for character in string.ascii_lowercase:
                if character == state[position]:
                    continue
                action = (position, character)
                if self.result(state, action) in dictionary:
                    allowed.append(action)
        return allowed

    def result(self, state, action):
        """ takes a state and an action and returns a new state """

        state_list = list(state)
        state_list[action[0]] = action[1]
        return ''.join(state_list)


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
            # just adding 1
            return c + 1
        elif self.cost == 'scrabble':
            # add value of new letter
            return c + scrabble[action[1]]
        elif self.cost == 'frequency':
            # add 1 plus rarity of new word
            return c + 1 + dictionary[state2]
        else:
            raise ValueError(f"unknown cost measure: {self.cost}")

    def __repr__(self):
        """" return a suitable string to represent this problem instance """

        return f"dc({self.initial},{self.goal},{self.cost})"

    def h(self, node):
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        state = node.state

        wrong = [i for i in range(len(state)) if state[i] != self.goal[i]]
        if not wrong:
            return 0
        if self.cost == 'steps':
            return len(wrong)
        elif self.cost == 'scrabble':
            return sum(scrabble[self.goal[i]] for i in wrong)
        elif self.cost == 'frequency':
            return (len(wrong) - 1) * (1 + min_rarity) + 1 + dictionary[self.goal]
        else:
            raise ValueError(f"unknown cost measure: {self.cost}")
