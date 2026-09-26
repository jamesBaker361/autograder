""" starter file for pa1: dogcat """

import search       # AIMA module for search problems
import gzip         # read from a gzip'd file
#name: Teras Abebe, CMSC471 1445, 
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
        if (len(initial) in [3,4] and initial.islower() and initial in dictionary):
            self.initial = initial 
        else:
            raise ValueError("Error, the entered initial is not valid")
        if (len(goal) == len(initial) and goal.islower() and goal in dictionary):
            self.goal = goal
        else:
            raise ValueError("Error,the entered goal is not valid length or not in dictionary")
        self.cost = cost

    def actions(self, state):
        return actionsDC(state)


    def result(self, state, action):
        return resultDC(state, action)

    def goal_test(self, state):
        return goal_testDC(state, self.goal)

    def path_cost(self, c, state1, action, state2):
        return path_costDC(c, state1, action, state2, self.cost)
        

    def __repr__(self):
        """" return a suitable string to represent this problem instance """
        return f"DC instance: initial={self.initial}, goal={self.goal}, cost={self.cost}"

    def h(self, node):
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        estCost = 0
        if node.state == self.goal:
            return estCost
        elif(self.cost == 'steps'):
            for i in range(len(node.state)):
                if(node.state[i] != self.goal[i]):
                    estCost += 1
            return estCost
        elif(self.cost == 'scrabble'):
            for i in range(len(node.state)):
                if(node.state[i] != self.goal[i]): 
                    estCost += letterValue([i, self.goal[i]])
            return estCost
        elif(self.cost == 'frequency'): #since we dont know future words, lower bound will be +1 for each word
            for i in range(len(node.state)):
                if(node.state[i] != self.goal[i]):
                    estCost += 1
            return (estCost + dictionary[self.goal])
        
            
    
def letterValue(action):
    cost = 0
    if(action[1] in ('a', 'e', 'i', 'o', 'u', 'l', 'n', 's', 't', 'r')):
        cost = 1
    elif(action[1] in ('d', 'g')):
        cost = 2
    elif(action[1] in ('b', 'c', 'm', 'p')):
        cost = 3
    elif(action[1] in ('f', 'h', 'v', 'w', 'y')):
        cost = 4
    elif(action[1] == 'k'):
        cost = 5
    elif(action[1] in ('j', 'x')):
        cost = 6
    elif(action[1] in ('q', 'z')):
        cost = 10
    return cost

def actionsDC(state):
    word_list = []
    temp = ""
    lowLetters = list("abcdefghijklmnopqrstuvwxyz")
    for i in range(len(state)):
        for z in range(len(lowLetters)):
            temp = state[:i] + lowLetters[z] + state[i+1:]
            if temp in dictionary and lowLetters[z] != state[i]:
                word_list.append([i, lowLetters[z]])
    return word_list

def resultDC(state, action):
    temp = state
    new_word = temp[:action[0]] + action[1] + temp[action[0]+1:]
    if state[action[0]] != action[1] and action[1].islower() and new_word in dictionary:
        return new_word
    raise ValueError("Invalid action")

def goal_testDC(state, goal):
    """True if state ==goal, false otherwise"""
    return state == goal
    
def path_costDC(c, state1, action, state2, cost):
    if(cost == 'steps'):
        c += 1 
    elif(cost == 'scrabble'):
        c += letterValue(action)
    elif(cost == 'frequency'):
        c += (1 + dictionary[state2])
    return c


    