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
    """DC is a subclass of the AIMA search files's Problem class. 
       Its init method takes three arguments: the initial word, goal word, and cost method.
       A state is represented as a lowercase string of three or four
       ascii characters.  Both the initial and goal states must be
       words of the same length and they must be in the dict
       dictionary. The cost argument specifies how to measure the
       cost of an action and can be 'steps', 'scrabble' or 'frequency'
       """

    def __init__(self, initial='dog', goal='cat', cost='steps'):
        #TODO: complete this
        # set instance attributes ...
        self.initial = initial.lower()
        self.goal = goal.lower()
        self.cost = cost.lower()
        pass
        if len(self.goal) != len(self.initial):
            raise ValueError("Initial and goal states must have the same length.")
        if len(self.goal) != 3 and len(self.goal) != 4:
            raise ValueError("Initial and goal states must be 3 or 4 letters long.")
        # make sure arguments are legal, raising an error if any are bad.
        if self.initial not in dictionary:
            raise ValueError(f"Initial state {self.initial} is not in the dictionary.")
        if self.goal not in dictionary:
            raise ValueError(f"Goal state {self.goal} is not in the dictionary.")
        if self.cost not in ['steps', 'scrabble', 'frequency']:
            raise ValueError(f"Cost method {self.cost} is not valid. Must be 'steps', 'scrabble', or 'frequency'.")
        pass

    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """
        # for each position in the word, iterate through all possible characters (lowercase)
        # and if a word is in the dictionary, is not the same as the current state, and brings
        # us closer to the goal, then add it to the list of possible actions
        valid_actions = []
        if len(state) == len(self.goal):   
            for i in range(len(state)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    if c == state[i]:
                        continue
                    new_word = state[:i] + c + state[i+1:]
                    if new_word in dictionary:
                        valid_actions.append((i, c))
        return valid_actions

    

    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        index, new_char = action
        new_state = state[:index] + new_char + state[index+1:]
        return new_state.lower()

    def goal_test(self, state):
        #TODO: complete this
        if self.goal == state:
            return True
        else:
            return False

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
            # Scrabble letter values
            scrabble_values = {
                'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1,
                'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 6,
                'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1,
                'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1,
                'u': 1, 'v': 4, 'w': 4, 'x': 6, 'y': 4,
                'z': 10
            }
            # Calculate the cost based on the letter that was changed
            new_letter = action[1]
            return c + scrabble_values[new_letter]
        elif self.cost == 'frequency':
            # Calculate the cost based on the rarity of the new word
            return c + (1 + dictionary[state2])
        else:
            raise ValueError(f"Unknown cost method: {self.cost}")
        pass

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

        mismatches = sum(1 for a, b in zip(node.state, self.goal) if a != b)
        if self.cost == 'steps':
            return mismatches
        elif self.cost == 'scrabble':
            return mismatches * 1  # Each mismatch costs at least 1 in scrabble
        elif self.cost == 'frequency':
            min_cost = min(dictionary.values())
            return (dictionary[self.goal] + (mismatches - 1) * min_cost)  # Each mismatch costs at least the minimum frequency of any word
            #return (mismatches + dictionary[self.goal])  # Each mismatch costs at least the frequency of the goal word
        else:
            raise ValueError(f"Unknown cost method: {self.cost}")
