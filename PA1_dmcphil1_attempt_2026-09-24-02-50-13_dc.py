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
        # set instance attributes ...
        self.initial = initial
        self.goal = goal
        self.cost = cost
        # make sure arguments are legal, raising an error if any are bad.
        if not isinstance(self.initial, str) or not isinstance(self.goal, str):
            raise ValueError("Arguments aren't strings")
        if not self.initial.islower() or not self.goal.islower():
            raise ValueError("Not lowercase strings")
        if len(self.initial) not in (3, 4) or len(self.goal) not in (3, 4):
            raise ValueError("Not 3- or 4-letter words")
        if len(self.initial) != len(self.goal):
            raise ValueError("Not the same length.")
        if self.initial not in dictionary or self.goal not in dictionary:
            raise ValueError("Not valid words in dictionary")
        # IMPORTANT: llm is Question 4 addition. h0 is the same as steps
        if self.cost not in ('steps', 'scrabble', 'frequency', 'llm'):
            raise ValueError("Incorrect method entered")

    def actions(self, state):
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """
        
        allowed_actions = [] # List of tuples, tuples have format (int, char)
        for i in range(len(state)):
            for char in "qwertyuiopasdfghjklzxcvbnm": # Importing string would be simpler
                # Skip matching character
                if char == state[i]:
                    continue
                # Make new word from initial's components and the selected letter
                new_word = state[:i] + char + state[i + 1:]
                # New "word" must be actual word in the dictionary
                if new_word in dictionary:
                    allowed_actions.append((i, char))
        return allowed_actions

    def result(self, state, action):
        """ takes a state and an action and returns a new state """
        if action in self.actions(state):
            new_pos, new_char = action
            # Make a new word based on existing state and action
            new_state = state[:new_pos] + new_char + state[new_pos + 1:]
            return new_state
        
    def goal_test(self, state):
        """ returns True iff state is a goal state for this problem instance """
        if state == self.goal:
            return True

    def path_cost(self, c, state1, action, state2):
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """
        if action in self.actions(state1):
            match self.cost:
                case 'steps':
                    # Every legal letter replacement costs 1
                    cost = 1
                case 'scrabble':
                    # Cost is determined by provided Scrabble value
                    cost = self.scrabble_value(action[1])
                case 'frequency' | 'llm':
                    # "Produces" word w means (state1, action) -> w/state2
                    # state2's rarity value is what gets used, then
                    cost = 1 + dictionary[state2]

        return c + cost

    def __repr__(self):
        """" return a suitable string to represent this problem instance """
        # Example output: DOGCAT(dog, cat, steps)
        return f"DOGCAT({self.initial}, {self.goal}, {self.cost})"

    def h(self, node):
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        # Returns 0 at the goal
        if self.goal == node.state:
            return 0
        elif self.cost == "steps":
            # Heuristic utilized: Comparing # of mismatched characters
            return self.mismatches(self.goal, node.state)
        elif self.cost == "scrabble":
            # Heuristic utilized: Comparing value of all the mismatched letters
            return self.mismatch_value(self.goal, node.state)
        elif self.cost == "frequency":
            # Heuristic utilized: Comparing current state to 
            # the dictionary word that has the lowest frequency
            return self.mismatches(self.goal, node.state) * (1 + min(dictionary.values()))
        # Added for Question 4
        elif self.cost == "llm":
            return self.llm_h(self.goal, node.state)
        
    # Auxiliary functions
    def scrabble_value(self, char):
        if char in "aeioulnstr":
            return 1
        elif char in "dg":
            return 2
        elif char in "bcmp":
            return 3
        elif char in "fhvwy":
            return 4
        elif char in "k": # I know it's weird, consistency matters more to me
            return 5
        elif char in "jx":
            return 6
        elif char in "qz":
            return 10

    def mismatches(self, state1, state2):
        num_mismatches = 0
        for char1, char2 in zip(state1, state2):
            if char1 != char2:
                num_mismatches += 1

        return num_mismatches

    def mismatch_value(self, state1, state2): #goal, node
        goal_value = 0
        for char1, char2 in zip(state1, state2):
            if char1 != char2:
                goal_value += self.scrabble_value(char1)

        return goal_value

    def llm_h(self, state1, state2): #goal, node
        h_dist = self.mismatches(state1, state2)
        rarity_g = dictionary[state1]
        if h_dist == 1:
            return h_dist + rarity_g
        # H(n,g) >= 2
        movements = self.actions(state2)
        neighbors = []
        for movement in movements:
            neighbors.append(self.result(state2, movement))
        min_neighbor_rarity = min(dictionary[val] for val in neighbors)
        min_global_rarity = min(dictionary.values())

        r_step = min_neighbor_rarity + (h_dist - 2) * min_global_rarity
        return h_dist + rarity_g + r_step