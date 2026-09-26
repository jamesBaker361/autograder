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

SCRABBLE_VALUES = {
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
        # validate metric argument
        if cost not in ('steps', 'scrabble', 'frequency'):
            raise ValueError(f"Invalid cost metric '{cost}'. Must be 'steps', 'scrabble', or 'frequency'.")

        #Validate string type and lowercase
        #both input arguments are strings
        if not isinstance(initial, str) or not isinstance(goal, str):
            raise TypeError("Initial and goal states must be strings.")
        # Ensure both words are formatted as lowercase strings
        if not initial.islower() or not goal.islower():
            raise ValueError("Initial and goal words must be lowercase.")

        #Validate word length
        if len(initial) not in (3, 4) or len(goal) not in (3, 4):
            raise ValueError("Words must be 3 or 4 letters long.")
        if len(initial) != len(goal):
            raise ValueError(f"Initial word length ({len(initial)}) must match goal word length ({len(goal)}).")

        #Validate presence in the global dictionary
        
        if initial not in dictionary:
            raise ValueError(f"Initial word '{initial}' is not in the dictionary.")
        if goal not in dictionary:
            raise ValueError(f"Goal word '{goal}' is not in the dictionary.")

        #Initialize base Problem class and assign instance attributes
        super().__init__(initial, goal)
        self.cost = cost









        

    def actions(self, state):
    
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        # Initialize a list
        valid_actions = []

        for pos in range(len(state)):
            # Store the current letter at this position
            current_char = state[pos]
            
            # Try substituting every letter from 'a' to 'z'
            for char in alphabet:
                # we only replace with a DIFFERENT letter[
                if char != current_char:
                    candidate_word = state[:pos] + char + state[pos + 1:]
                    
                    # Check if the generated word exists 
                    if candidate_word in dictionary:
                        # Store the action as a tuple
                        valid_actions.append((pos, char))

        # Return the list 
        return valid_actions

        

    def result(self, state, action):
        
        """ takes a state and an action and returns a new state """
        pos, char = action
        #return the new state word
        return state[:pos] + char + state[pos + 1:]

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
            step_cost = 1

        elif self.cost == 'scrabble':
           
            _, char = action
            # Step cost is the Scrabble point value 
            step_cost = SCRABBLE_VALUES[char]

        elif self.cost == 'frequency':
            # Step cost is 1 + rarity
            step_cost = 1.0 + dictionary[state2]

        else:
            step_cost = 1

        # Return cumulative cost to reach state2
        return c + step_cost

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

        # Find all character positions, current state differs from goal state

        mismatched_indices = [i for i in range(len(state)) if state[i] != self.goal[i]]
        num_mismatches = len(mismatched_indices)

        if self.cost == 'steps':
            # Minimum moves needed is equal to the number of mismatched characters
            return num_mismatches

        elif self.cost == 'scrabble':
            # Lower bound is the sum of Scrabble values of all target characters needed
            return sum(SCRABBLE_VALUES[self.goal[i]] for i in mismatched_indices)

        elif self.cost == 'frequency':
            # Minimum moves needed equals num_mismatches
            return float(num_mismatches)

        return 0

        
