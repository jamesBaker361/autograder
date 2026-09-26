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

print(dictionary['cat'], dictionary['hat'])

# cost of replacing a letter with each of these letters, for the scrabble cost measure 
scrabble_value = {
    'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1, 'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
    'd': 2, 'g': 2,
    'b': 3, 'c': 3, 'm': 3, 'p': 3,
    'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
    'k': 5,
    'j': 6, 'x': 6,
    'q': 10, 'z': 10
}

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
        # check that both words are lowercase, 3 or 4 letters, and in the dictionary
        for word in (initial, goal):
            if word != word.lower():
                raise ValueError(word + " must be lowercase")
            if len(word) != 3 and len(word) != 4:
                raise ValueError(word + " must be 3 or 4 letters long")
            if word not in dictionary:
                raise ValueError(word + " is not in the dictionary")

        if len(initial) != len(goal):
            raise ValueError("initial and goal must be the same length")

        if cost != "steps" and cost != "scrabble" and cost != "frequency":
            raise ValueError("cost must be steps, scrabble, or frequency")

        super().__init__(initial, goal)
        self.cost = cost

    def actions(self, state):
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        alphabet = "abcdefghijklmnopqrstuvwxyz"
        acts = []
        for i in range(len(state)):
            for letter in alphabet:
                if letter == state[i]:
                    continue
                new_word = state[:i] + letter + state[i+1:]
                if new_word in dictionary:
                    acts.append((i, letter))
        return acts

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
        if self.cost == "steps":
            return c + 1
        elif self.cost == "scrabble":
            i, letter = action
            return c + scrabble_value[letter]
        elif self.cost == "frequency":
            return c + 1 + dictionary[state2]

    def __repr__(self):
        """" return a suitable string to represent this problem instance """
        return "dc(" + self.initial + "," + self.goal + "," + self.cost + ")"

    def h(self, node):
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        state = node.state

        # count the number of letter positions that still differ from
        # the goal; each one needs at least one more action to fix
        diff = 0
        for i in range(len(state)):
            if state[i] != self.goal[i]:
                diff += 1

        if self.cost == "steps":
            # every action costs exactly 1, so diff actions cost diff
            return diff
        elif self.cost == "scrabble":
            # the cheapest possible replacement letter costs 1
            # (a, e, i, o, u, l, n, s, t, r), so diff actions cost at least diff
            return diff * 1
        elif self.cost == "frequency":
            # the cheapest possible action costs 1 (rarity is never negative),
            # so diff actions cost at least diff
            return diff * 1


class DCR(DC):
    """Same as DC, but uses the rarity-aware heuristic h_R
       for the frequency cost measure."""

    def __init__(self, initial='dog', goal='cat', cost='steps'):
        super().__init__(initial, goal, cost)
        # smallest dictionary number among words the same length as the goal
        L = len(goal)
        self.r_min = min(v for w, v in dictionary.items() if len(w) == L)

    def h(self, node):
        # for steps and scrabble, just use the original heuristic
        if self.cost != "frequency":
            return super().h(node)

        state = node.state
        if state == self.goal:
            return 0

        # count letters that still differ from the goal
        diff = 0
        for i in range(len(state)):
            if state[i] != self.goal[i]:
                diff += 1

        # last move must land on the goal (exact cost);
        # every other move costs at least 1 + r_min
        return (1 + dictionary[self.goal]) + (diff - 1) * (1 + self.r_min)
