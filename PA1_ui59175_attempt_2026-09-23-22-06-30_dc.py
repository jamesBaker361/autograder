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
        #initial and goal are strings
        if type(initial)  != str or type(goal) != str:
            raise ValueError("Initial and goal must be strings")

        #Words are lowercase
        if initial != initial.lower() or goal != goal.lower():
            raise ValueError("Words must be lowercase")

        #Words have length 3 or 4
        if len(initial) not in (3, 4) or len(goal) not in (3, 4):
            raise ValueError("Words must have 3 or 4 letters")

        #initilal and goal have the same length
        if len(initial) != len(goal):
            raise ValueError("Initial and goal must have the same length")

        #words are in the dictionary
        if initial not in dictionary or goal not in dictionary:
            raise ValueError("Words must be in the dictionary")

        #cost is valid
        if cost not in ('steps', 'scrabble', 'frequency'):
            raise ValueError("Invalid cost")
        
       
        
        self.initial = initial
        self.goal = goal
        self.cost = cost

    def actions(self, state):
        #Changing one letter at a time and words need to be in the dictionary

        actions = []
        for pos in range(len(state)):
            for letter in "abcdefghijklmnopqrstuvwxyz":
                if letter == state[pos]: #a letter should not replace itself
                    continue
                new_word = state[:pos] + letter + state[pos+1:]
                if new_word in dictionary:
                    actions.append((pos, letter))
        return actions


    def result(self, state, action):
        
        """ takes a state and an action and returns a new state """
        pos, letter = action
        new_word = state[:pos] + letter + state[pos+1:]
        return new_word

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
      
        if self.cost == 'steps': #Each letter change cost = 1
            return c + 1

        elif self.cost == 'scrabble':# Each letter change cost is the provided scrabble value
            pos, letter = action

            if letter in "aeioulnstr":
                value = 1
            elif letter in "dg":
                value = 2
            elif letter in "bcmp":
                value = 3
            elif letter in "fhvwy":
                value = 4
            elif letter in "k":
                value = 5
            elif letter in "jx":
                value = 6
            elif letter in "qz":
                value = 10

            return c + value
            
       
        elif self.cost == 'frequency':
            rarity = dictionary[state2]
            return c + 1 + rarity

    def __repr__(self):
        return "Initial: " + self.initial + ", Goal: " + self.goal + ", Cost: " + self.cost
    
    def h(self, node):
        
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        state = node.state
       
        if state == self.goal: #h(goal)=0
            return 0

        #count of number of positions that differ from the goal for Steps, Scrabble and Frequency cost 
        
        if self.cost == 'steps': 
            count = 0

            for i in range(len(state)):
                if state[i] != self.goal[i]:
                    count += 1
            return count

        elif self.cost == 'scrabble':
            total = 0

            for i in range(len(state)):
                if state[i] != self.goal[i]:
                    letter = self.goal[i]

                    if letter in "aeioulnstr":
                        value = 1
                    elif letter in "dg":
                        value = 2
                    elif letter in "bcmp":
                        value = 3
                    elif letter in "fhvwy":
                        value = 4
                    elif letter in "k":
                        value = 5
                    elif letter in "jx":
                        value = 6
                    elif letter in "qz":
                        value = 10

                    total += value

            return total

        elif self.cost == 'frequency':
            count = 0

            for i in range(len(state)):
                if state[i] != self.goal[i]:
                    count += 1
            
                      
            return count 
        
            




       

