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
        if len(initial) != len(goal):
            raise ValueError("Lengths of the words are different")
        
        if initial not in dictionary:
            raise ValueError("Initial word not in dictionary")

        if not initial.islower():
            raise ValueError("Initial word must be lowercase")
        
        if goal not in dictionary:
            raise ValueError("Goal word not in dictionary")
        
        if not goal.islower():
            raise ValueError("Initial word must be lowercase")

        if cost != 'steps' and cost != 'scrabble' and cost != 'frequency':
            raise ValueError("Cost is not valid")
        
        self.initial= initial
        self.goal= goal
        self.cost= cost
        """
        #TODO: complete this
        # set inst*ance attributes ...
        pass
        # make sure arguments are legal, raising an error if any are bad.
        pass
        """
    
    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        alphabet= "abcdefghijklmnopqrstuvwxyz"
        legal= []
        for i in range(len(state)):
            for letter in alphabet:
                if letter != state[i]:
                    new_word = state[:i] + letter + state[i+1:]
                    if new_word in dictionary:
                        legal.append((i, letter))

        return legal

    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        if len(action) == 2:
            position, letter= action
        else:
            raise ValueError(f"Bad action: {action}")

        if (position < len(state)) and (position >= 0):
            new_word = state[:position] + letter + state[position+1:]
            state= new_word
            return state

        else:
            raise ValueError(f"Bad action: {action}")
        #pass

    def goal_test(self, state):
        #TODO: complete this
        """ returns True iff state is a goal state for this problem instance 
        """
        goal_state= self.goal
        return (goal_state == state)
        #pass

    def path_cost(self, c, state1, action, state2):
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """
        path= self.cost
        if path == 'steps':
            return c + 1
            
        elif path == 'scrabble':
            for i in range(len(state1)):
                if state1[i] != state2[i]:
                    if state2[i] in "aeioulnstr":
                        c= c + 1
                    elif state2[i] in "dg":
                        c= c + 2
                    elif state2[i] in "bcmp":
                        c= c + 3
                    elif state2[i] in "fhvwy":
                        c= c + 4
                    elif state2[i] == "k":
                        c= c + 5
                    elif state2[i] in "jx":
                        c= c + 6
                    elif state2[i] in "qz":
                        c= c + 10
            return c
        elif path == 'frequency':
            for i in range(len(state1)):
                if state1[i] != state2[i]:
                    c= c + 1 + dictionary[state2]
            return c
        else:
            raise ValueError(f"Cost invalid")
        
        #pass

    def __repr__(self):
        #TODO: complete this
        """" return a suitable string to represent this problem instance """
        return f"DC({self.initial},{self.goal},{self.cost})"
        #pass

    def h(self, node):
        #TODO: complete this
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        state= node.state

        letters=0
        for i in range(len(state)):
            if state[i] != self.goal[i]:
                letters+= 1

        if letters == 0:
            return letters

        elif self.cost == 'steps':
            return letters

        elif self.cost == 'scrabble':
            total= 0
            for i in range(len(state)):
                if state[i] != self.goal[i]:
                    if self.goal[i] in "aeioulnstr":
                        total= total + 1
                    elif self.goal[i] in "dg":
                        total= total + 2
                    elif self.goal[i] in "bcmp":
                        total= total + 3
                    elif self.goal[i] in "fhvwy":
                        total= total + 4
                    elif self.goal[i] == "k":
                        total= total + 5
                    elif self.goal[i] in "jx":
                        total= total + 6
                    elif self.goal[i] in "qz":
                        total= total + 10

            return total
        
        elif self.cost == 'frequency':
                # Goal state


            # h0: number of letters that are different
            different = 0

            for i in range(len(state)):
                if state[i] != self.goal[i]:
                    different += 1

            # Find the smallest rarity among all legal one-letter neighbors
            min_rarity = float('inf')

            for word, rarity in dictionary.items():

                # Count how many letters are different
                differences = 0

                for i in range(len(state)):
                    if state[i] != word[i]:
                        differences += 1

                # A legal action changes exactly one letter
                if differences == 1:
                    if rarity < min_rarity:
                        min_rarity = rarity

            return different + min_rarity

        #pass
