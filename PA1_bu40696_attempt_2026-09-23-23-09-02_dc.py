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
        #TODO: complete this
        # set instance attributes ...

        self.initial = initial
        self.goal = goal
        self.cost = cost

    

        # make sure arguments are legal, raising an error if any are bad.
        # Initial and goal must be strings
        if not isinstance(initial, str) or not isinstance(goal, str):
          raise ValueError("Initial and goal must be strings")

        # Initial and goal must be lowercase
        if initial.lower() != initial or goal.lower() != goal:
          raise ValueError("Initial and goal must be lowercase")

        # Words must be 3 or 4 letters long
        if len(initial) not in (3, 4) or len(goal) not in (3, 4):
          raise ValueError("Initial and goal must be 3 or 4 letters long")

        # Initial and goal must have the same length
        if len(initial) != len(goal):
          raise ValueError("Initial and goal must have the same length")

        # Both words must exist in the supplied dictionary
        if initial not in dictionary or goal not in dictionary:
          raise ValueError("Initial and goal must be legal dictionary words")

        # Cost must be one of the three supported cost measures
        if cost not in ('steps', 'scrabble', 'frequency'):
          raise ValueError("Cost must be steps, scrabble, or frequency")

        

    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """
        actions = []

        # Go through each position in the word
        for i in range(len(state)):

          # Try every lowercase letter
          for letter in 'abcdefghijklmnopqrstuvwxyz':

            # Don't replace a letter with itself
            if letter == state[i]:
              continue

            # Create the new word
            new_word = state[:i] + letter + state[i+1:]

            # Only allow it if it is a legal dictionary word
            if new_word in dictionary:
              actions.append((i, letter))
        
        return actions


  

    def result(self, state, action):
      #TODO: complete this
      """ takes a state and an action and returns a new state """
      position, letter = action

      new_state = state[:position] + letter + state[position+1:]

      return new_state


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
          position, letter = action

          scrabble_values = {'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1,
            'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
            'd': 2, 'g': 2,
            'b': 3, 'c': 3, 'm': 3, 'p': 3,
            'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
            'k': 5,
            'j': 6, 'x': 6,
            'q': 10, 'z': 10
            }

          return c + scrabble_values[letter]

        elif self.cost == 'frequency':
          return c + 1 + dictionary[state2]


    def __repr__(self):
        #TODO: complete this
        """ return a suitable string to represent this problem instance """
        return f"DC({self.initial}, {self.goal}, {self.cost})"
        

    def h(self, node):
        #TODO: complete this
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        state = node.state

        # Find positions where current word differs from goal
        differences = 0
        for i in range(len(state)):
            if state[i] != self.goal[i]:
                differences += 1

        # Steps: each wrong position requires at least one action
        if self.cost == 'steps':
            return differences

        # Scrabble: each wrong position must eventually
        # receive its corresponding goal letter
        elif self.cost == 'scrabble':
            scrabble_values = {
                'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1,
                'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
                'd': 2, 'g': 2,
                'b': 3, 'c': 3, 'm': 3, 'p': 3,
                'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
                'k': 5,
                'j': 6, 'x': 6,
                'q': 10, 'z': 10
            }

            estimate = 0

            for i in range(len(state)):
                if state[i] != self.goal[i]:
                    estimate += scrabble_values[self.goal[i]]

            return estimate

        # Frequency: every action costs at least 1
        elif self.cost == 'frequency':
            return differences