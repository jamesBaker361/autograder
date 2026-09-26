""" starter file for pa1: dogcat """

import search       # AIMA module for search problems
import gzip
import string   

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

scrabble_values = {
    **{letter: 1 for letter in "aeioulnstr"},
    **{letter: 2 for letter in "dg"},
    **{letter: 3 for letter in "bcmp"},
    **{letter: 4 for letter in "fhvwy"},
    "k": 5,
    **{letter: 6 for letter in "jx"},
    **{letter: 10 for letter in "qz"}
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
        ##: complete this
        # set instance attributes ...
        
        # make sure arguments are legal, raising an error if any are bad.
        if not isinstance(initial, str) or not isinstance(goal, str):
            raise ValueError("Both words must be strings")

        if initial not in dictionary:
            raise ValueError("Invalid initial word")

        if goal not in dictionary:
            raise ValueError("Invalid goal word")

        if len(initial) != len(goal):
            raise ValueError("IWords must be the same lengthh")

        if len(initial) not in [3, 4]:
            raise ValueError("Words must contain 3 or 4 letters")

        if cost not in ["steps", "scrabble", "frequency"]:
            raise ValueError("Invalid cost method")

        super().__init__(initial, goal)
        self.cost = cost
            
        

    def actions(self, state):
      
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        legal_actions = []

        for position in range(len(state)):
            for letter in string.ascii_lowercase:

                if letter == state[position]:
                    continue

                new_word = (
                    state[:position]
                    + letter
                    + state[position + 1:]
                )

                if new_word in dictionary:
                    legal_actions.append((position, letter))

        return legal_actions


    
        
        

    def result(self, state, action):
      
        """ takes a state and an action and returns a new state """
        position, letter = action

        return (
            state[:position]
            + letter
            + state[position + 1:]
        )



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
            letter = action[1]
            return c + scrabble_values[letter]

        elif self.cost == "frequency":
            return c + 1 + dictionary[state2]


        

    def __repr__(self):
       
        """" return a suitable string to represent this problem instance """
        return f"DC({self.initial},{self.goal},{self.cost})"

    def h(self, node):
        
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        state = node.state

        if state == self.goal:
         return 0

        mismatches = sum(
            current_letter != goal_letter
            for current_letter, goal_letter in zip(state, self.goal)
         )

        if self.cost == "steps":
         return mismatches

        elif self.cost == "scrabble":
            scrabble_estimate = 0

            for current_letter, goal_letter in zip(state, self.goal):
                if current_letter != goal_letter:
                 scrabble_estimate += scrabble_values[goal_letter]

                 return scrabble_estimate

        elif self.cost == "frequency":
         return mismatches

