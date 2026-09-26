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
        # validate arguments first
        # check if the string is lowercase
        if initial.islower() == False or goal.islower() == False:
            raise ValueError("Words must be all lowercase.")

        # check if initial and goal words are equal length
        if len(initial) != len(goal):
            raise ValueError("Initial and goal must have the same length.")
        
        # check if word length is not equal to 3 or 4 (not allowed)
        if len(initial) not in (3, 4) or len(goal) not in (3, 4):
            raise ValueError("Words must be 3 or 4 letters long.")

        # check if goal and initial word is in given dictionary
        if goal not in dictionary:
            raise ValueError("Goal word not in dictionary.")

        if initial not in dictionary:
            raise ValueError("Initial word not a valid word.")

        # make sure cost argument is one of 3 values steps, scrabble, or frequency
        if cost not in ("steps", "scrabble", "frequency"):
            raise ValueError("Cost argument is invalid.")
    
        # initialize variables
        self.initial = initial
        self.goal = goal
        self.cost = cost
        self.dict = dictionary

        # also make scrabble cost cost dictionary for the lettrs, used later mainly in cost path!
        scrabbleScores = {
            'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1, 'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
            'd': 2, 'g': 2,
            'b': 3, 'c': 3, 'm': 3, 'p': 3,
            'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
            'k': 5,
            'j': 6, 'x': 6,
            'q': 10, 'z': 10 
            }

        # save for later
        self.scrabbleScores = scrabbleScores

        # call parent constructor
        super().__init__(initial, goal) 
    
    def actions(self, state):
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """

        # make list of all alphabet characters
        alphabet = list(map(chr, range(97, 123))) 

        # initialize list for all possible next actions
        nextAction = []

        # for every character in the state word
        for i in range(len(state)):
            # iterate through every letter in the alphabet
            for x in alphabet:
                # replace that character with the alphabet letter
                # to avoid .replace replacing more than one letter, 
                # take all letters before index i + alphabet letter x + rest of word
                # to create the new word
                temp = state[:i] + x + state[i + 1:]
                # is the word a valid word in dictionary?
                if temp in self.dict:
                    # as long as the temp word does not equal initial word, add it to list
                    if temp != state:
                        nextAction.append(temp);

        # print list of valid next actions
        return nextAction

    def result(self, state, action):
        """ takes a state and an action and returns a new state """
        return action

    def goal_test(self, state):
        """ returns True if state is a goal state for this problem instance """
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """

        if self.cost == "steps":
            # each cost is 1
            return c + 1
        
        elif self.cost == "scrabble":
            # find which letter changed
            for i in range(len(state1)):
                if state1[i] != state2[i]:
                    new_letter = state2[i]
                    # get the score and return
                    return c + self.scrabbleScores[new_letter]

        elif self.cost == "frequency":
            # score based on dictionary
            return c + self.dict[action]

        else:
            raise ValueError("Invalid cost measure.")


    def __repr__(self):
        """" return a suitable string to represent this problem instance """
        return f"DC(initial={self.initial}, goal={self.goal}, cost={self.cost})"

    def h(self, node):
        state = node.state

        # if already at goal
        if state == self.goal:
            return 0

        # mismatch count (h0)
        mismatches = 0
        for i in range(len(state)):
            if state[i] != self.goal[i]:
                mismatches += 1

        # compute r_min directly here
        r_min = min(self.dict.values())

        # compute rarity(goal) directly here
        rarity_goal = self.dict[self.goal]

        # final hr formula
        return (mismatches - 1) * (1 + r_min) + (1 + rarity_goal)


    ## def h(self, node):
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        state = node.state
        goal = self.goal
        wordLength = len(state)
        # find how many letter mismatches are in the string ONLY IF the letter is different than the goal
        mismatches = sum(1 for i in range(len(state)) if state[i] != goal[i])

        # if the cost is through steps, a good way to measure
        # h is how many more letters need to change to get goal word
        if self.cost == "steps":
            return mismatches

        elif self.cost == "scrabble":
            # initialize total to 0 first
            total = 0

            # check every letter
            for i in range(wordLength):
                # if they are not the same, take the goal word letter
                # find out what its cost is, add it total, then return total
                if state[i] != goal[i]:
                    neededLetter = goal[i]
                    total += self.scrabbleScores[neededLetter]
                
            return total
        
        # honestly i just did this to maintain lower bound and couldnt think of a better way
        # you could also average the frequencies of all possible words
        # from inital word but that could make h > true cost?
        elif self.cost == "frequency":
            return mismatches
##
