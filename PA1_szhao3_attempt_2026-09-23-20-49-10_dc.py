""" starter file for pa1: dogcat """

import search       # AIMA module for search problems
import gzip         # read from a gzip'd file
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


VALID_COSTS = {'steps', 'scrabble', 'frequency'}

SCRABBLE_LETTER_COST = {} 
for replaceLetters, cost in [
    ('aeioulnstr', 1),
    ('dg', 2),
    ('bcmp', 3),
    ('fhvwy', 4),
    ('k', 5),
    ('jx', 6),
    ('qz', 10)
]:
    for letter in replaceLetters:
        SCRABBLE_LETTER_COST[letter] = cost

#1 + rarity(w), costs associated for a word are in dictionary
FREQUENCY_COST_MIN = 1 + min(dictionary.values())


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

        """
        lowercase strings, 3-4 letters, goal and init is same, in words34
        cost must be valid 
        """
        minLength = 3
        maxLength = 4

        for word in initial, goal:
            if not(word.islower()) or not(word.isalpha):
                raise ValueError("Words have to be all lowercase and may not contain numbers.")

            if len(word) < minLength and len(word) > maxLength:
                raise ValueError("Words have to be between 3-4 letters.")

            if word not in dictionary:
                raise ValueError("Words have to be in the dictionary")

        if len(initial) != len (goal):
            raise ValueError("Goal and initial word have to be same length")

        if cost not in VALID_COSTS:
            raise ValueError("Costs must be valid")

        self.initial = initial
        self.goal = goal
        self.cost = cost


        # pass
        # # make sure arguments are legal, raising an error if any are bad.
        # pass

    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        #(State, action)
        #action --> (index, letter)
        actions = []

        for index in range(len(state)):
            for letter in string.ascii_lowercase:
                if state[index] != letter:
                    candidateWord = state[:index] + letter + state[index + 1:]
                    if candidateWord in dictionary:
                        actions.append((index, letter))

        return actions



    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        index, letter = action
        newWord = state[:index] + letter + state[index + 1:]

        return newWord 
    

    def goal_test(self, state):
        #TODO: complete this
        """ returns True iff state is a goal state for this problem instance """
        if state == self.goal:
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

        cost = 0

        if self.cost == 'steps':
            cost = c + 1
            return cost
        elif self.cost == 'scrabble':
            index, letter = action
            cost = c + SCRABBLE_LETTER_COST[letter]
            return cost
        elif self.cost == 'frequency':
            cost = c + 1 + dictionary[state2]
            return cost
        else:
            return cost
        

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
        #search.py line 80 for node object
        state = node.state
        goal = self.goal
        mismatches = 0

        for index in range(len(state)):
            letterState = state[index]
            letterGoal = goal[index]
            if letterState != letterGoal:
                mismatches += 1
        

        if mismatches == 0:
            return 0

        if self.cost == 'steps':
            #mismatches also indicates the least number of actions
            #required to get to the goal from current state.
            return mismatches
        
        elif self.cost == 'scrabble':
            total = 0
            #sum of the goal letters because that is minimum needed
            #cost to reach the goal
            for i in range(len(state)):
                if state[i] != goal[i]:
                    total += SCRABBLE_LETTER_COST[goal[i]]
            return total

        elif self.cost == 'frequency':
            """
            regardless of the new word, the cost is at least that of the 
            smallest rarity value in the dictionary. I multiply it by 
            the number of mismatches currently becuase no matter what 
            that will be how many actions there will be
            """
            return mismatches * FREQUENCY_COST_MIN


