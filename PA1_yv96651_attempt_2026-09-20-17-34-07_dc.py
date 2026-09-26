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
        self.initial = initial
        self.goal = goal
        self.cost = cost
        # make sure arguments are legal, raising an error if any are bad.
        # legnth checking both words
        if len(initial) < 3:
            raise ValueError("Initial word is too short in length!")
        if len(initial) > 4:
            raise ValueError("Initial word is too long in length!")
        if len(goal) < 3:
            raise ValueError("Goal word is too short in length!")
        if len(goal) > 4:
            raise ValueError("Goal word is too long in length!")
        # length comparing both words - needs matching length
        if len(initial) != len(goal):
            raise ValueError("Length of Initial Word and Goal Word must match!")
        # lowercase check
        if not initial.islower() or not goal.islower():
            raise ValueError("Both words must be in lowercase letters!")
        # dictionary check
        if not initial in dictionary:
            raise ValueError("Initial word not found in dictionary!")
        if not goal in dictionary:
            raise ValueError("Goal word not found in dictionary!")

    def actions(self, state):
        words = [] # List for storing all possible state changes from current state
        for i in range(len(state)):
            for c in "abcdefghijklmnopqrstuvwxyz": # get all letters 

                # create a new word with the replacement character at state[i]
                word = state[:i] + c + state[i+1:]

                # skip if created word matches "state" word
                if word == state:
                    continue

                # add to list if created word is in the dictionary
                if word in dictionary:
                    words.append(word)

        return words

    def result(self, state, action):
        return action

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        if self.cost == "steps":
            c += 1
        elif self.cost == "scrabble":
            changed = self.find_changed_letter(state1, state2)
            c += self.get_scrabble_cost(changed)
        elif self.cost == "frequency":
            c += (1 + dictionary[state2])

        return c

    # Helper method to find the changed letter between 2 words for the scrabble cost
    def find_changed_letter(self, state1, state2):
        for i in range(len(state1)): # both words are the same length
            if(state1[i] != state2[i]):
                return state2[i]
        return

    # Helper method to obtain scrabble cost for individual characters
    def get_scrabble_cost(self, char):
        if char in "aeioulnstr":
            return 1
        elif char in "dg":
            return 2
        elif char in "bcmp":
            return 3
        elif char in "fhvwy":
            return 4
        elif char == "k":
            return 5
        elif char in "jx":
            return 6
        elif char in "qz":
            return 10
        return

    def __repr__(self):
        return f"Changing the initial word {self.initial} --> {self.goal} using a {self.cost} cost measurement"

    def h(self, node):
        count = 0 # cost estimate counter
        if self.cost == "steps":
            for char1, char2 in zip(node.state, self.goal):
                if char1 != char2:
                    count += 1
        elif self.cost == "scrabble":
            for char1, char2 in zip(node.state, self.goal):
                if char1 != char2:
                    count += self.get_scrabble_cost(char2)
        elif self.cost == "frequency":
            for char1, char2 in zip(node.state, self.goal):
                # frequency cost is similar to steps cost (use steps cost as a baseline cost)
                if char1 != char2:
                    count += 1 
            # but we can also account for the rarity of the goal word
            # as "remaining work that at least needs to be done"
            count += dictionary[self.goal]

        return count