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

# Scrabble tile values for each letter (used in path_cost and h)
SCRABBLE_VALUES = {
    'a':1,'e':1,'i':1,'o':1,'u':1,'l':1,'n':1,'s':1,'t':1,'r':1,
    'd':2,'g':2,
    'b':3,'c':3,'m':3,'p':3,
    'f':4,'h':4,'v':4,'w':4,'y':4,
    'k':5,
    'j':6,'x':6,
    'q':10,'z':10
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
        #TODO: complete this
        # set instance attributes ...
        self.cost = cost
        # make sure arguments are legal, raising an error if any are bad.
        assert isinstance(initial, str) and initial.islower(), \
            f"initial word '{initial}' must be a lowercase string"
        assert isinstance(goal, str) and goal.islower(), \
            f"goal word '{goal}' must be a lowercase string"
        assert len(initial) in (3, 4), \
            f"initial word '{initial}' must be 3 or 4 letters"
        assert len(initial) == len(goal), \
            f"initial '{initial}' and goal '{goal}' must have the same length"
        assert initial in dictionary, \
            f"initial word '{initial}' is not in the dictionary"
        assert goal in dictionary, \
            f"goal word '{goal}' is not in the dictionary"
        assert cost in ('steps', 'scrabble', 'frequency'), \
            f"cost must be 'steps', 'scrabble', or 'frequency', got '{cost}'"
        # call the parent Problem __init__ which stores self.initial and self.goal
        super().__init__(initial, goal)

    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """
        legal = []
        for pos in range(len(state)):
            for char in 'abcdefghijklmnopqrstuvwxyz':
                # skip if the replacement character is the same as current
                if char != state[pos]:
                    new_word = state[:pos] + char + state[pos+1:]
                    # only include if the resulting word is in the dictionary
                    if new_word in dictionary:
                        legal.append((pos, char))
        return legal

    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        pos, char = action
        return state[:pos] + char + state[pos+1:]

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
        pos, char = action
        if self.cost == 'steps':
            # every action costs exactly 1
            return c + 1
        elif self.cost == 'scrabble':
            # cost is the scrabble value of the replacement letter
            return c + SCRABBLE_VALUES[char]
        elif self.cost == 'frequency':
            # cost is 1 + the rarity value of the resulting word
            return c + 1 + dictionary[state2]

    def __repr__(self):
        #TODO: complete this
        """" return a suitable string to represent this problem instance """
        return f"dc({self.initial},{self.goal},{self.cost})"

    def h(self, node):
        #TODO: complete this
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        # count positions where the current state differs from the goal
        mismatches = sum(c1 != c2 for c1, c2 in zip(node.state, self.goal))
        if self.cost == 'steps':
            # each mismatched position needs at least 1 more action
            return mismatches
        elif self.cost == 'scrabble':
            # the cheapest possible scrabble letter is 1, so mismatches * 1
            # is a safe lower bound on remaining scrabble cost
            return mismatches
        elif self.cost == 'frequency':
            # each remaining step costs at least 1 (since rarity >= 0),
            # so mismatches * 1 is a safe lower bound on remaining frequency cost
            return mismatches