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

        self.initial = initial #Initializing
        self.goal = goal
        self.cost = cost

        #Checking if inputted words and costs are legal.
        if len(goal) != len(initial): 
            raise ValueError('Both words must be equal length')

        if len(initial) not in [3, 4]:
            raise ValueError('Initial word can only be 3 or 4 letters.')

        if len(goal) not in [3, 4]:
            raise ValueError('Goal word can only be 3 or 4 letters.')
        
        if initial not in dictionary:
            raise ValueError('Initial word must be in dictionary.')
        
        if goal not in dictionary:
            raise ValueError('Goal word must be in dictionary.')

        if cost not in ['steps', 'scrabble', 'frequency']:
            raise ValueError('Invalid cost argument.')



    def actions(self, state):
        #TODO: complete this
       
        alphabet = 'abcdefghijklmnopqrstuvwxyz' #Alphabet list
        action_list = [] #List to put actions in

        for letter_num in range(len(state)): #Gets every possible legal move from current state, puts it into action list then returns it.
            for alphabet_letter in alphabet:
                if alphabet_letter != state[letter_num]:

                    new_state = self.replace_letter(state, alphabet_letter, letter_num)

                    if new_state in dictionary:
                        action_list.append((letter_num, alphabet_letter))
        return action_list


    def result(self, state, action): #Takes state and action and returns new state.
        position, letter = action
        return self.replace_letter(state, letter, position)


    def goal_test(self, state): #Returns true if inputted state is the goal state.
        return state == self.goal

    def path_cost(self, c, state1, action, state2): #Returns path cost depending on cost scheme.
        if self.cost == 'steps': 
            return c + 1 #Cost for each letter shift is 1

        elif self.cost == 'scrabble':
            return c + self.get_scrabble_value(action[1]) #Cost for each letter shift is scrabble value.

        elif self.cost == 'frequency':
            return c + 1 + dictionary[state2] #Cost for each letter shift is the frequency of next word + 1

        raise ValueError('Invalid cost argument.')




    def __repr__(self): #Returns a string to represent problem instance.
        return f'Initial state: {self.initial} Final state: {self.goal} Cost measure: {self.cost}'

    def h(self, node):
        #TODO: complete this
        #Returns heuristic, the estimate of cost to get to goal node from the current node.
    
        
        if node.state == self.goal: #Returns 0 if node is already at goal.
            return 0

        h_cost = 0
        for position in range(len(self.goal)): #Counts number of letter positions that differ, if cost is scrabble, h_cost takes into account letter cost as well.
            if node.state[position] != self.goal[position]:
                if self.cost == 'scrabble':
                    h_cost += self.get_scrabble_value(self.goal[position])
                else:
                    h_cost += 1
                    
       
        if self.cost == 'steps' or self.cost == 'scrabble': 
            return h_cost

        elif self.cost == 'frequency':

            
            frequency_list = [] #finds all possible moves that lead to legal words and their frequencies
            action_list = self.actions(node.state)
            for action in action_list:
                word = self.result(node.state, action)
                frequency_list.append(dictionary[word])

            return h_cost + min(frequency_list) #Number of incorrect letter positions + cost (frequency) of the cheapest possible move that can be taken
            
            #return h_cost * (1 + min(dictionary.values()))
            #AI generated Heuristic for problem 4.


        


        raise ValueError('Invalid cost argument.') #Only reachable if cost scheme is invalid

    def replace_letter(self, word, letter, position): #Replaces one letter of a string in a particular position.
        word = list(word)
        word[position] = letter
        return ''.join(word)
    
    def get_scrabble_value(self, letter): #Returns scrabble letter cost for a letter
        scrabble_values = {
            'a': 1,
            'b': 3,
            'c': 3,
            'd': 2,
            'e': 1,
            'f': 4,
            'g': 2,
            'h': 4,
            'i': 1,          
            'j': 6,
            'k': 5,
            'l': 1,
            'm': 3,
            'n': 1,
            'o': 1,
            'p': 3,
            'q': 10,
            'r': 1,           
            's': 1,
            't': 1,
            'u': 1,
            'v': 4,
            'w': 4,
            'x': 6,
            'y': 4,
            'z': 10,
        }

        if letter in scrabble_values:
            return scrabble_values[letter]

        else:
            raise ValueError('Invalid scrabble input.')



