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

REPLACEMENT_COSTS = {
    "aeioulnstr": 1,
    "dg": 2,
    "bcmp": 3,
    "fhvwy": 4,
    "k": 5,
    "jx": 6,
    "qz": 10
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
        self.initial = initial
        self.goal = goal
        self.cost = cost
        # make sure arguments are legal, raising an error if any are bad.
        #• be lowercase strings;
        if(not(isinstance(initial, str) and isinstance(goal,str) and isinstance(cost,str))):
            raise TypeError("initial, goal, and cost must be strings")

        if not(initial.islower() and goal.islower()):
            raise ValueError("initial and goal words must be lowercase")
        #• contain either three or four letters;
        #• have the same length; and
        if (not(3<=len(initial)<=4 and 3<=len(goal)<=4) or len(initial) != len(goal)):
            raise ValueError("initial and goal words must be 3 or 4 letters and must have the same length")
        
        #• appear in the provided dictionary
        if initial not in dictionary or goal not in dictionary:
            raise KeyError("initial or goal word not in dictionary")

        costs = ['steps', 'scrabble', 'frequency']
        if cost not in costs:
            raise ValueError("illegal cost")

        

    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """
        ALPHABET = "abcdefghijklmnopqrstuvwxyz"
        possible_actions = []
        new_state = state
        for pos in range(len(state)):
            for char in ALPHABET:
                if(char == state[pos]):
                    continue
                new_state = state[:pos] + char + state[pos+1:]
                if(new_state in dictionary):
                    possible_actions.append((pos, char))

        return possible_actions

    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        return state[:action[0]] + action[1] + state[action[0]+1:]

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
        # • steps: add 1;
        # • scrabble: add the assigned value of the newly inserted letter; or
        # • frequency: add 1 + rarity(𝑤), where 𝑤 is the resulting word

        if(self.cost == "steps"):
            return c+1
        elif(self.cost == "scrabble"):
            for key in REPLACEMENT_COSTS:
                if(action[1] in key):
                    return c + REPLACEMENT_COSTS[key]
        elif(self.cost == "frequency"):
            return c + 1 + dictionary[state2]

    def __repr__(self):
        #TODO: complete this
        """" return a suitable string to represent this problem instance """
        return f"initial: {self.initial} \ngoal: {self.goal}\ncost measure: {self.cost}"

    def h(self, node):
        #TODO: complete this
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        #calculate number of incorrect letters
        if(self.cost == "steps"):
            bad_letters = 0
            for pos in range(len(self.goal)):
                bad_letters += (self.goal[pos] != node.state[pos])
            return bad_letters
        elif self.cost == "scrabble":
            #get incorrect letter positions
            #calculate the scrabble for the letters that need to be replaced
            need_cost = 0
            for pos in range(len(node.state)):
                if node.state[pos] != self.goal[pos]:
                    for key in REPLACEMENT_COSTS:
                        if self.goal[pos] in key:
                            need_cost += REPLACEMENT_COSTS[key]
                            break
            return need_cost
        elif self.cost == "frequency":
            #return absolute minimum cost possible if you can change all the letters at once
            return 0 if self.goal_test(node.state) else (1 + dictionary[self.goal])
            
           

    def print_rarity(self, state1, state2):
        print(f'{state1}: {dictionary[state1]}\n{state2}: {dictionary[state2]}')


   