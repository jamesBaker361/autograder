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

    # I COMPLETED
    def __init__(self, initial='dog', goal='cat', cost='steps'):
        #TODO: complete this
        # set instance attributes ...
        if type(initial) != str or type(goal) != str:
            raise ValueError("Initial and Goal words must be strings")
        
        i = len(initial)
        g = len(goal)

        #print(dictionary)


        # make sure arguments are legal, raising an error if any are bad.
        if (i, g) not in [(3, 3), (4, 4)]:
            raise ValueError("Initial and Goal words must be same length (3s or 4s)")
        if initial != initial.lower() or goal != goal.lower():
            raise ValueError("Initial and Goal words must be lowercase")
        if initial not in dictionary or goal not in dictionary:
            raise ValueError("Invalid Initial or Goal word (not in dictionary)")
        if cost not in ['steps', 'scrabble', 'frequency']:
            raise ValueError("Cost is not one of the supported arguments")

        # set instance attributes if valid
        self.initial = initial
        self.goal = goal
        self.cost = cost
        

    # maybe fix this to use a dictionary idk?
    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """
        possible = []
        words = []
        letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        current = list(state)
        action = list(state)
        #print(f"CURRENT: {current}")
        #print(f"FIRST ACTION: {action}")
        for i in range(len(current)):
            for x in letters:
                action[i] = x
                word = "".join(action)
                #print(f"ACTION: {word}")
                if word in dictionary and word not in words and word != state:
                    words.append(word)
                    possible.append(str(i) + x)
            action = list(state)
                
        #print(f"POSSIBLE: {possible}")
        #print(f"WORDS: {words}")
        return possible

    # DOUBLE CHECK - rewrite to use action like 0d or 1f to mean change index 0 to d or change index 1 to f?
    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """

        word = list(state)
        word[int(action[0])] = action[1]
        return "".join(word)

    # COMPLETED
    def goal_test(self, state):
        #TODO: complete this
        """ returns True iff state is a goal state for this problem instance """
        return state == self.goal

    # DOUBLE CHECK (ask about what action means, i think that action and state2 are the same)
    # COMPLETED i think
    def path_cost(self, c, state1, action, state2):
        #TODO: complete this
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """

        scrabble_costs = {1: ["a","e","i","o","u","l","n","s","t","r"],
                          2: ["d","g"],
                          3: ["b","c","m","p"],
                          4: ["f","h","v","w","y"],
                          5: ["k"],
                          6: ["j","x"],
                          10: ["q","z"]}
        # verify that state 1 and state 2 are valid
        word = list(state1)
        word[int(action[0])] = action[1]
        combined = "".join(word)
        if combined != state2 or combined not in dictionary:
            return c

        # steps behavior
        if self.cost == "steps":
            return c + 1

        # scrabble behavior
        elif self.cost == "scrabble":

            # get that letter's value
            cost = 0
            for value in scrabble_costs:
                if action[1] in scrabble_costs[value]:
                    cost = value

            return c + cost
            
        # frequency behavior
        elif self.cost == "frequency":
            return c + 1 + dictionary[state2]
        else:
            return c
        
    # DONE
    def __repr__(self):
        #TODO: complete this
        """" return a suitable string to represent this problem instance """
        return f"dc({self.initial},{self.goal},{self.cost})"

    # DONE
    def h(self, node):
        #TODO: complete this
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        scrabble_costs = {1: ["a","e","i","o","u","l","n","s","t","r"],
                                  2: ["d","g"],
                                  3: ["b","c","m","p"],
                                  4: ["f","h","v","w","y"],
                                  5: ["k"],
                                  6: ["j","x"],
                                  10: ["q","z"]}

        state = node.state
        #print(f"STATE: {state}")

        wrong_counter = 0
        for l in range(len(state)):
            if state[l] != self.goal[l]:
                wrong_counter += 1
                
        if self.cost == "steps":
            return wrong_counter
            
        elif self.cost == "scrabble":
            cost_counter = 0
            for l in range(len(state)):
                char = self.goal[l]
                if state[l] != char:

                    # find the cost of right letter
                    for value in scrabble_costs:
                        if char in scrabble_costs[value]:
                            cost_counter += value
            return cost_counter
                    
        elif self.cost == "frequency":

            # already at goal state
            if wrong_counter == 0:
                return 0

            # for written part question 4
            minimum = 100
            for key in dictionary:
                if dictionary[key] < minimum:
                    minimum = dictionary[key]
            
            # the frequency cost will be at least 1 and need the rarity of the goal state
            return wrong_counter + dictionary[self.goal] #+ (wrong_counter * minimum)

