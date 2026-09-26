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

# Cost of the most frequent word in the dictionary
MOSTFREQUENTWORDVALUE = dictionary[list(dictionary.keys())[0]]

# Dictionary of the scrabble cost for each letter
scrabbleCost = {"a": 1, "e": 1, "i": 1, "o": 1, "u": 1, "l": 1, "n": 1, "s": 1, "t": 1, 
                "r": 1, "d": 2, "g": 2, "b": 3, "c": 3, "m": 3, "p": 3, "f": 4, "h": 4, 
                "v": 4, "w": 4, "y": 4, "k": 5, "j": 6, "x": 6, "q": 10, "z": 10}

# List of all letters
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
           "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
           "y", "z"]

class InvalidWordError(Exception):
    pass
class InvalidSizeError(Exception):
    pass
class InvalidCostError(Exception):
    pass

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
        # Makes the inputted variables lowercase in case they aren't and gets the length of the words
        initialTest = initial.lower()
        goalTest = goal.lower()
        costTest = cost.lower()
        inLength = len(initialTest)
        goalLength = len(goalTest)

        # Checks if the initial or goal word isn't in the dictionary and raises an exception 
        # if not
        if (initialTest not in dictionary):
            print("The initial word is not a valid word.")
            raise InvalidWordError
        elif (goalTest not in dictionary):
            print("The initial word is not a valid word.")
            raise InvalidWordError

        # If the initial word and goal word aren't 3 or 4 letters and not the same length, it 
        # raises an exception
        elif (inLength != goalLength):
            print("The initial word and goal word are not the same length.")
            raise InvalidSizeError
        elif (inLength > 4 or inLength < 3):
            print("The initial and goal word must be length 3 or 4.")
            raise InvalidSizeError

        # If the cost is not a valid cost type, it raises an exception
        elif (costTest != "steps" and costTest != "scrabble" and costTest != "frequency"):
            print("Please enter a valid cost type (steps, scrabble, or frequency).")
            raise InvalidCostError

        # If those tests all pass, it sets the initial and goal words and the cost to the 
        # inputted values
        else:
            self.initial = initialTest
            self.goal = goalTest
            self.cost = costTest

    def actions(self, state):
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        # List of all the valid letters that can be switched out for the 
        # letter of the corresponding spot
        actionList = []

        # For each letter in current word, it searches through each letter 
        # that isn't the same one as the current letter to see if it can 
        # make a valid word. For all that do, it adds that letter into the 
        # spot of actionList.
        for i in range(len(state)):
            for letter in letters:
                if (state[i] != letter):
                    newWord = self.makeNewWord(state, letter, i)
                    if (newWord in dictionary):
                        actionList.append(str(letter + str(i)))

        # Returns the calculated list of actions
        return actionList

    def result(self, state, action):
        """ takes a state and an action and returns a new state """
        return self.makeNewWord(state, action[0], int(action[1]))

    def goal_test(self, state):
        """ returns True iff state is a goal state for this problem instance """
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """
        if (self.cost == "steps"):
            return c + 1
        elif (self.cost == "scrabble"):
            return c + scrabbleCost[action[0]]
        else:
            return c + 1 + dictionary[state2]

    def __repr__(self):
        """" return a suitable string to represent this problem instance """
        return ("dc(" + self.initial + ", " + self.goal + ", " + self.cost + ")")

    def h(self, node):
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        # Gets the word of the current node, the goal word, and the parent word
        currWord = node.state
        goalWord = self.goal

        # Option to use the AI-made heuristic for the frequency cost measure
        useAiHeuristic = True

        # Checks to see if the current word is actually the goal word, and returns 0 
        # if so.
        if (currWord == goalWord):
            return 0

        # For saving the current heuristic cost total
        sumCost = 0

        # If the cost type is steps, it adds 1 to the heuristic value for each
        # incorrect letter in the current word
        if (self.cost == "steps"):
            for i in range(len(currWord)):
                if (currWord[i] != goalWord[i]):
                    sumCost += 1

        # If the cost type is scrabble, for each incorrect letter in the current word,
        # it adds the scrabble cost value for the corresponding correct letter in the
        # goal word
        elif (self.cost == "scrabble"):
            for i in range(len(currWord)):
                if (currWord[i] != goalWord[i]):
                    sumCost += scrabbleCost[goalWord[i]]

        # If the cost type is frequency, for each incorrect letter in the current word, 
        # it adds 1 to the cost. Afterwards, it multiplies that number minus 1 by the 
        # cheapest frequency cost in the dictionary, and then adds the cost of changing 
        # to the goal word. Since the number of mismatched letters is always 1 or more, 
        # since if it was 0, it would be equal to the goal word, it will always be 
        # positive.
        elif (not useAiHeuristic):
            for i in range(len(currWord)):
                if (currWord[i] != goalWord[i]):
                    sumCost += 1
            sumCost = (sumCost - 1) * (1 + MOSTFREQUENTWORDVALUE)
            sumCost += (1 + dictionary[goalWord])

        # If the cost type is frequency and the AI heuristic is on, it uses the AI-made 
        # heuristic.
        else:
            for i in range(len(currWord)):
                if (currWord[i] != goalWord[i]):
                    sumCost += 1
            if (sumCost == 1):
                return (1 + dictionary[goalWord])

            actionList = self.actions(currWord)
            neighborList = []
    
            for action in actionList:
                neighborWord = self.result(currWord, action)
                neighborList.append(dictionary[neighborWord])
    
            smallestFrequencyCost = 20
            for i in range(len(neighborList)):
                if (neighborList[i] < smallestFrequencyCost):
                    smallestFrequencyCost = neighborList[i]

            sumCost = sumCost + smallestFrequencyCost + dictionary[goalWord]

        # Returns the calculated heuristic value
        return sumCost

    def makeNewWord(self, word, letter, spot):
        # Makes a new word where the inputted letter replaces the letter in the 
        # inputted spot of the inputted word and returns it.
        if (spot == 0):
            newWord = letter + word[1:]
        elif (spot == 1):
            newWord = word[0] + letter + word[2:]
        elif (spot == 2):
            newWord = word[:2] + letter
            if (len(word) == 4):
                newWord += word[3]
        elif (spot == 3):
            newWord = word[:3] + letter
        return newWord