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

# scrabble values for each letter, got it from the table in the assignment pdf
SCRABBLE_VALUES = {'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1, 'l': 1, 'n': 1,'s': 1, 't': 1, 'r': 1, 'd': 2, 'g': 2, 'b': 3, 'c': 3, 'm': 3, 'p': 3, 'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4, 'k': 5, 'j': 6, 'x': 6, 'q': 10, 'z': 10}

# for the frequency heuristic.  For every word length, position, and
# letter, MIN_RARITY holds the smallest rarity of any word that has
# that letter at that position.  So, the cheapest 3 letter word
# with 'k' in spot 2.  I fill this in once at startup with one loop
# over the whole dictionary, so h() can just look it up.
MIN_RARITY = {}
for word in dictionary:

    r = dictionary[word]

    for i in range(len(word)):

        key = (len(word), i, word[i])

        if key not in MIN_RARITY or r < MIN_RARITY[key]:

            MIN_RARITY[key] = r


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
        
        # make sure arguments are legal, raising an error if any are bad.

        # check the two words first
        for word in (initial, goal):

            if type(word) != str:

                raise ValueError("word must be a string")

            if word != word.lower():

                raise ValueError(word + " must be lowercase")

            if not word.isalpha():

                raise ValueError(word + " must have letters only")

            if len(word) != 3 and len(word) != 4:

                raise ValueError(word + " must be 3 or 4 letters long")

            if word not in dictionary:

                raise ValueError(word + " is not in the dictionary")

        # the two words have to be the same length
        if len(initial) != len(goal):

            raise ValueError("initial and goal must be the same length")

        # cost has to be one of the three names we support
        if cost != 'steps' and cost != 'scrabble' and cost != 'frequency':

            raise ValueError("cost must be 'steps', 'scrabble' or 'frequency'")

        self.initial = initial
        self.goal = goal
        self.cost = cost

    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        # an action is a (position, letter) pair.  Try every position
        # with every letter, keep the ones that give a real word.
        possible = []
        for i in range(len(state)):

            for letter in SCRABBLE_VALUES:

                if letter != state[i]:

                    new_word = state[:i] + letter + state[i+1:]

                    if new_word in dictionary:

                        possible.append((i, letter))

        return possible

    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        i, letter = action

        return state[:i] + letter + state[i+1:]

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
        if self.cost == 'steps':

            return c + 1

        elif self.cost == 'scrabble':

            # cost of an action is the value of the new letter
            return c + SCRABBLE_VALUES[action[1]]

        else:
            # frequency: entering word state2 costs 1 plus its rarity
            return c + 1 + dictionary[state2]

    def __repr__(self):
        #TODO: complete this
        """ return a suitable string to represent this problem instance """
        return f"dc({self.initial},{self.goal},{self.cost})"

    def h(self, node):
        #TODO: complete this
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal.

        All three versions use the same idea.  Every position where the
        word is different from the goal has to be changed at some point,
        and look at the LAST time each of those positions gets changed:
        after that change it already has the goal letter, so that one
        action must cost at least some minimum amount.  Different
        positions are changed by different actions, so I can just add up
        a minimum cost for each wrong position.  That sum can never be
        more than the real remaining cost, so the heuristic is
        admissible.
        """
        state = node.state
        goal = self.goal
        total = 0

        for i in range(len(state)):

            if state[i] != goal[i]:

                if self.cost == 'steps':
                    # at least one action per wrong position
                    total = total + 1

                elif self.cost == 'scrabble':
                    # last change there must put in goal[i], which is
                    # worth scrabble_values[goal[i]]
                    total = total + SCRABBLE_VALUES[goal[i]]

                else:
                    # last change there makes some word with goal[i] in
                    # spot i, and the cheapest such word costs
                    # 1 + MIN_RARITY (looked up from my table)
                    total = total + 1 + MIN_RARITY[(len(state), i, goal[i])]

        return total
