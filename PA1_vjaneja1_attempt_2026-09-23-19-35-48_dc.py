""" starter file for pa1: dogcat """

# Viraj Janeja - MON/WED 4pm section



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
        self.state = initial
        self.actions(initial)
        
        # make sure arguments are legal, raising an error if any are bad.
        if((initial not in dictionary) or (goal not in dictionary)):
            raise Exception("Both the initial and goal word should be valid words.")
        costs = ['steps', 'scrabble', 'frequency']
        if(cost not in costs):
            raise Exception("Please enter a valid cost type")

    def actions(self, state):
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """
        actionsList = []
        for i in range(len(state)):
            curChar = state[i]
            for j in range(26):
                a=97
                c = chr(a+j)
                if(not(c == curChar)):
                    temp = state
                    temp = list(temp)
                    temp[i] = c
                    temp = "".join(temp)
                    if(temp in dictionary):
                        newAction = [i, c]
                        actionsList.append(newAction)
        return actionsList



    def result(self, state, action):
        """ takes a state and an action and returns a new state """
        stateL = list(state)
        stateL[action[0]] = action[1]
        self.state = "".join(stateL)
        return self.state

    def goal_test(self, state):
        """ returns True iff state is a goal state for this problem instance """
        return (state == self.goal)

    def path_cost(self, c, state1, action, state2):
        #TODO: complete this
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """
        if(self.cost == "steps"):
            return (c+1)
        elif(self.cost == "scrabble"):
            return (c+self.getScrabbleVal(action[1]))
        else:
            return (c+1+dictionary[state2])
        

    def __repr__(self):
        #TODO: complete this
        """" return a suitable string to represent this problem instance """
        return f"{self.initial} --> {self.goal} ; With cost measure: {self.cost} ;"
        

    def h(self, node):
        #TODO: complete this
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """
        result = 0
        current = list(node.state)
        goal = list(self.goal)
        if(current == goal):
            return result
        elif(self.cost == "steps"):
            for i in range(len(current)):
                if(current[i] != goal[i]):
                    result += 1
            return result
        elif(self.cost == "scrabble"):
            for i in range(len(goal)):
                if(current[i] != goal[i]):
                    result += self.getScrabbleVal(goal[i])
            return result
        else:
            result = 0
            for i in range(len(current)):
                if(current[i] != goal[i]):
                    result += 1
            result += dictionary[self.goal]
            return result

    def getScrabbleVal(self, letter):
        letter = letter.upper()
        one = [1, 'A', 'E', 'I', 'O', 'U', 'L', 'N', 'S', 'T', 'R']
        two = [2, 'D', 'G']
        three = [3, 'B', 'C', 'M', 'P']
        four = [4, 'F', 'H', 'V', 'W', 'Y']
        five = [5, 'K']
        six = [6, 'J', 'X']
        ten = [10, 'Q', 'Z']
        letters = [one, two, three, four, five, six, ten]
        for l in letters:
            if(letter in l):
                return (l[0])
        print(f"weird scrabble letter: -{letter}-")
        return 0




