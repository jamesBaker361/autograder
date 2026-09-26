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

scrabble_table = {

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



class DC(search.Problem):

    def __init__(self, initial='dog', goal='cat', cost='steps'):

        if not (3 <= len(initial) <= 4) or not (3 <= len(goal) <= 4):
            raise ValueError("Arg length for initial and goal must be 3 or 4 characters long")
        if (len(initial) != len(goal)):
            raise ValueError("Character lengths for initial and goal must be the same")
        if  not initial.islower() or not goal.islower():
            raise ValueError("Initial and Goal must be lowercase")
        if initial not in dictionary or goal not in dictionary:
            raise ValueError("Initial and Goal must be in the dictionary")

        self.initial = initial
        self.goal = goal

        if cost.casefold() not in ["steps", "scrabble", "frequency"]:
            raise ValueError("Cost method must be 'steps' or 'scrabble' or 'frequency'")
        else:
            self.cost = cost.casefold()



    def actions(self, state):

        stateList = []

        for i in range(len(state)):
            for letter in "abcdefghijklmnopqrstuvwxyz":
                if letter == state[i]:
                    continue

                new_word = state[:i] + letter + state[i+1:]

                if new_word in dictionary:
                    stateList.append((i, letter))

        return stateList



    def result(self, state, action):

        #unpack the tuple from actions()
        index, letter = action

        return state[:index] + letter + state[index+1:]



    def goal_test(self, state):

        return state == self.goal



    def path_cost(self, c, state1, action, state2):

        if self.cost == "steps":
            return self.steps_calculation(c, state1, action, state2)

        elif self.cost == "scrabble":
            return self.scrabble_calculation(c, state1, action, state2)

        else:
            return self.frequency_calculation(c, state1, action, state2)



    def __repr__(self):

        return f"dc({self.initial},{self.goal},{self.cost})"





    def h(self, node):

        if self.cost == "steps":
            return self.h_steps_calculation(node)

        if self.cost == "scrabble":
            return self.h_scrabble_calculation(node)

        if self.cost == "frequency":
            return self.h_frequency_calculation(node)



    def steps_calculation(self, c, state1, action, state2):

        return c + 1



    def scrabble_calculation(self, c, state1, action, state2):

        # using '_' will let me unpack the tuple without caring about the index because python is cool
        # and I don't need it for calculating cost
        _, letter = action

        action_cost = scrabble_table[letter]

        return c + action_cost



    # state2 is *not* the goal state, it is the next state provided in the sequence of nodes performed
    # by search algorithms, so even though it is calculating the rarity of a given word, it is not immediately
    # transforming the current state to the goal state. It calculates the rarity cost of the state2 argument
    # for each state transition that is being considered during the search
    def frequency_calculation(self, c, state1, action, state2):

        rarity_cost = dictionary[state2]

        return c + 1 + rarity_cost



    def h_steps_calculation(self, node):

        h_cost = 0

        for i in range(len(node.state)):
            if node.state[i] != self.goal[i]:
                h_cost += 1

        return h_cost



    def h_scrabble_calculation(self, node):
        h_cost = 0

        for i in range(len(node.state)):
            if node.state[i] != self.goal[i]:
                h_cost += scrabble_table[self.goal[i]]

        return h_cost



    # naive approach was to calculate the cost of each letter change corresponding to the cheapest word
    # in the dictionary (if node.state[i] != self.goal[i], find the cheapest word that would bring
    # node.state one step closer to goal. But the issue is that node.state[i+1] could have a cheaper path
    # to self.goal than node.state[i], and thus we may not then accurately calculate a true lower bound.
    # But since the rarity calculation is 1 + rarity, at minimum a change with frequency cost will always
    # provide at least 1 cost. So using the same equation as steps_calculation provides a reasonable, if still
    # naive approximation, to use as a heuristic. There is likely a margin of error here that could be accounted
    # for, but I think without understanding how the rarity itself is calculated, I can't make an informed decision
    # for a stronger heuristic.

    # Change note: The dictionary has a minimum rarity value, I can use that as a sum with the minimum cost 1 and
    # provide the sum as a scalar with the number of incorrect nodes. (abc) -> (efg) => 3 * (1 + MIN_RARITY)
    def h_frequency_calculation(self, node):

        MIN_RARITY = min(dictionary.values())

        h_cost = 0

        for i in range(len(node.state)):
            if node.state[i] != self.goal[i]:
                h_cost += 1

        return h_cost * (1 + MIN_RARITY)


    def AI_h_frequency_calculation(self, node):

        rarities = sorted(dictionary.values())

        h_cost = sum(
            node.state[i] != self.goal[i]
            for i in range(len(node.state))
        )

        cumulative_rarities = sum(rarities[:h_cost])

        return h_cost + cumulative_rarities