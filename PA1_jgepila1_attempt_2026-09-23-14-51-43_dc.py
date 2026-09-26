""" starter file for pa1: dogcat """

import string
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

# assigning scrabble letter values
# for scrabble cost heuristic and actions
SCRABBLE_VALUE = {}
for letters, value in [('aeioulnstr', 1),
                        ('dg', 2),
                        ('bcmp', 3),
                        ('fhvwy', 4),
                        ('k', 5),
                        ('jx', 6),
                        ('qz', 10)]:
    for ch in letters:
        SCRABBLE_VALUE[ch] = value

# helper function
# precompute the minimum word rarity for 3 and 4 letter words
# this gives us the lowest possible rarity so we can calculate
# the minimum action cost for the frequency heuristic
MIN_RARITY_BY_LENGTH = {}
for _length in (3, 4):
    _rarities = [r for w, r in dictionary.items() if len(w) == _length]
    MIN_RARITY_BY_LENGTH[_length] = min(_rarities) if _rarities else 0.0


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

        # validate all arguments
        # if there are any errors we raise an error w/
        # error message

        if not isinstance(initial, str) or not isinstance(goal, str):
            raise ValueError("initial word and state word must be strings")

        if initial != initial.lower() or goal != goal.lower():
            raise ValueError("initial word and goal word must be lowercase")

        if len(initial) not in (3, 4):
            raise ValueError("words must be three or four letters long")

        if len(initial) != len(goal):
            raise ValueError("initial word and goal word must be the same length")

        if initial not in dictionary:
            raise ValueError(f"initial word {initial!r} is not in the dictionary")

        if goal not in dictionary:
            raise ValueError(f"goal word {goal!r} is not in the dictionary")

        if cost not in ('steps', 'scrabble', 'frequency'):
            raise ValueError("cost must be 'steps', 'scrabble', or 'frequency'")

        # we pass all validation edits
        # we then initialize all variables in the class
        self.initial = initial
        self.goal = goal
        self.cost = cost


    def actions(self, state):
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        possible_actions = []
        for i in range(len(state)):
            for ch in string.ascii_lowercase:

                # skip replacing a letter with itself
                if ch == state[i]:
                    continue

                # check if the new word is in the dictionary
                candidate = state[:i] + ch + state[i + 1:]
                if candidate in dictionary:
                    possible_actions.append((i, ch))

        return possible_actions


    def result(self, state, action):
        """ takes a state and an action and returns a new state """

        i, ch = action
        return state[:i] + ch + state[i + 1:]


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
            i, ch = action
            return c + SCRABBLE_VALUE[ch]

        elif self.cost == 'frequency':
            return c + 1 + dictionary[state2]


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
        mismatches = [i for i in range(len(state)) if state[i] != self.goal[i]]
        n = len(mismatches)

        if n == 0:
            return 0

        if self.cost == 'steps':

            # mismatched letters is the number of steps
            # needed to get to the correct placing of the letters
            # therefore we return n
            
            return n

        elif self.cost == 'scrabble':
            
            # costs of actions is determined by the value
            # replacement of the letter
            # so for every letter we have to replace, we take the scrabble cost
            # and add that up to get the total cost

            return sum(SCRABBLE_VALUE[self.goal[i]] for i in mismatches)

        elif self.cost == 'frequency':

            # cost of actions is determined by 1 + rarity of the word
            # so for the n mismatched letters, we take the cost of reaching the goal
            # plus the minimum word cost for the other n - 1 steps to get the total cost

            min_rarity = MIN_RARITY_BY_LENGTH[len(state)]
            other_actions_min = (n - 1) * (1 + min_rarity)
            final_action_cost = 1 + dictionary[self.goal] # actual cost
            return other_actions_min + final_action_cost