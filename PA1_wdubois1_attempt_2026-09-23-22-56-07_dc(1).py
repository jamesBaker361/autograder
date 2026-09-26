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

#Scrabble letter costs from the assignment
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

        #make sure initial and goal types ar evalidated
        if not isinstance(initial, str) or not isinstance(goal, str):
            raise ValueError("initial type and goal type must both be strings")

        #make sure both the words are lowercase
        if initial != initial.lower() or goal != goal.lower():
            raise ValueError("Both intial type and goal type must be lowercase")

        #make sure words have a length of 3 or 4
        if len(initial) not in (3, 4) or len(goal) not in (3, 4):
            raise ValueError("Length of initial type and goal type must be 3 or 4 letters")

        #make sure words have the same length
        if len(initial) != len(goal):
            raise ValueError("Initial  and goal must be the same length (3 or 4)")

        #make sure both words are legal dictionary words
        if initial not in dictionary or goal not in dictionary:
            raise ValueError("The initial and goal must be in the dictionary")

        #make sure the cost is validated and checked
        if cost not in ('steps', 'scrabble', 'frequency'):
            raise ValueError("cost must be steps, scrabble, or frequency")


        #intiialize problem values
        super().__init__(initial, goal)

        #save the cost method that gets chosen
        self.cost = cost
        # pass
        # make sure arguments are legal, raising an error if any are bad.
        # pass

    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """


        legal_actions = []

        alphabet = 'abcdefghijklmnopqrstuvwxyz'

        #try to replace each position 
        for position in range(len(state)):

            #try each possible replacement fr the letters
            for letter in alphabet:

                #dont replace like characters with one another
                if letter == state[position]:
                    continue

                new_word = (state[:position] + letter + state[position + 1:])

                #only keep transformatiosn that keep legal words
                if new_word in dictionary:
                    legal_actions.append((position, letter))

        return legal_actions
    
        # pass

    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        position, letter = action

        return (state[:position] + letter + state[position + 1:])
        # pass

    def goal_test(self, state):
        #TODO: complete this
        """ returns True iff state is a goal state for this problem instance """
        return state == self.goal
        # pass

    def path_cost(self, c, state1, action, state2):
        #TODO: complete this
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """
        #every action will cost 1
        if self.cost == 'steps':
            return c + 1

        #cost is the scrabbble value of the letter being inserted 
        if self.cost == 'scrabble':
            replacement_letter = action[1]

            return c + scrabble_values[replacement_letter]

        #enteering state 2 cost
        return c + 1 + dictionary[state2]
        # pass

    def __repr__(self):
        #TODO: complete this
        """" return a suitable string to represent this problem instance """
        return f"dc({self.initial}, {self.goal}, {self.cost})"
        # pass

    def h(self, node):
        #TODO: complete this
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        #estimaet remaining cost of from the node to the goal
        state = node.state

        #find all the positions that are different from the goal
        mismatches = [i for i in range (len(state)) if state[i] != self.goal[i]]

        d = len(mismatches)

        #ath the goal there is no remaining cost left
        if d == 0:
            return 0

        #every mismathced position must get changed atleast once
        if self.cost == 'steps':
            return d

        #every incorrect position must eventually get its correpsonding goal letter 
        #also add the scrabble cost of the goal letters that cant be avoided
        if self.cost == 'scrabble':
            return sum(scrabble_values[self.goal[i]] for i in mismatches)

        # pass

        #final action is to enter the goal word 
        return d + dictionary[self.goal]
