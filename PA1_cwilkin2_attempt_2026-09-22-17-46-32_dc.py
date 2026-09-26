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
        #TODO: complete this
        # set instance attributes ...
        m_initial = initial
        m_goal = goal
        m_cost = cost

        # make sure arguments are legal, raising an error if any are bad.
        if m_initial not in dictionary or not isinstance(m_initial, str) or not m_initial.islower() or len(m_initial) < 3 or len(m_initial) > 4 or len(m_initial) != len(m_goal):
            raise ValueError
        if m_goal not in dictionary or not isinstance(m_goal, str) or not m_goal.islower() or len(m_goal) < 3 or len(m_goal) > 4:
            raise ValueError
        if m_cost not in ["steps", "scrabble", "frequency"]:
            raise ValueError

        super().__init__(m_initial, m_goal)
        self.cost = m_cost

        return

    def actions(self, state):
        #TODO: complete this
        """ Given a state (i.e., a word), return a list or iterator of
        all possible next actions.  An action is defined by position
        in the word and a character to put in that position.  But the
        result must be a legal word, i.e., in our dictionary, and it
        should not be the same as the state, i.e., don't replace a
        character with the same character """
        alpha = "abcdefghijklmnopqrstuvwxyz"
        answers = []
        for i in range(len(state)):
            for each in alpha:
                state_split = list(state)
                state_split[i] = each
                curr = "".join(state_split)
                if curr in dictionary and curr != state:
                    answers.append((i, each))
        return answers

    def result(self, state, action):
        #TODO: complete this
        """ takes a state and an action and returns a new state """
        state_split = list(state)
        index, letter = action
        state_split[index] = letter
        state = "".join(state_split)
        return state

    def goal_test(self, state):
        #TODO: complete this
        """ returns True iff state is a goal state for this problem instance """
        if state == self.goal:
            return True
        return False

    def path_cost(self, c, state1, action, state2):
        #TODO: complete this
        """ Returns the cost to get to state2 by applying action in
        state1 given that c is the cost to get up to state1. For the 
        the dc problem, you will have to check what
        cost metric (self.cost) is being used for this problem instance,
        i.e., is it steps, scrabble or frequency """
        if self.cost == "steps":
            c += 1
            return c
        elif self.cost == "scrabble":
            index, letter = action
            if letter in "aeioulnstr":
                c += 1
                return c
            elif letter in "dg":
                c += 2
                return c
            elif letter in "bcmp":
                c += 3
                return c
            elif letter in "fhvwy":
                c += 4
                return c
            elif letter in "k":
                c += 5
                return c
            elif letter in "jx":
                c += 6
                return c
            elif letter in "qz":
                c += 10
                return c
            return c
        elif self.cost == "frequency":
            c += dictionary[state2]
            c += 1
            return c
        return c

    def __repr__(self):
        #TODO: complete this
        """" return a suitable string to represent this problem instance """
        return f"dc({self.initial},{self.goal},{self.cost})"

    def h(self, node):
        #TODO: complete this
        """Heuristic: returns an estimate of the cost to get from the
        state of the node to the goal state. The heuristic's value should
        depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
        or frequency), as this will effect the estimate cost to get to
        the nearest goal. """

        state_split = list(node.state)
        goal_split = list(self.goal)

        if self.cost == "steps":
            count_wrong = 0
            for index in range(len(state_split)):
                if state_split[index] != goal_split[index]:
                    count_wrong += 1
            return count_wrong
        
        elif self.cost == "scrabble":
            cost_total = 0
            for index in range(len(state_split)):
                if state_split[index] != goal_split[index]:
                    letter = goal_split[index]
                    if letter in "aeioulnstr":
                        cost_total += 1
                    elif letter in "dg":
                        cost_total += 2
                    elif letter in "bcmp":
                        cost_total += 3
                    elif letter in "fhvwy":
                        cost_total += 4
                    elif letter in "k":
                        cost_total += 5
                    elif letter in "jx":
                        cost_total += 6
                    elif letter in "qz":
                        cost_total += 10
            return cost_total

        elif self.cost == "frequency":
            # New Version
            # dist = 0
            # for index in range(len(state_split)):
            #     if state_split[index] != goal_split[index]:
            #         dist +=1
            # cost_total = dist

            # for k in range(dist):
            #     min_rarity = -1

            #     for word in dictionary:
            #         if len(word) != len(self.goal):
            #             continue

            #         word_dist = 0
            #         for index in range(len(word)):
            #             if word[index] != self.goal[index]:
            #                 word_dist += 1

            #         if word_dist == k:
            #             if min_rarity == -1 or dictionary[word] < min_rarity:
            #                 min_rarity = dictionary[word]

            #     if min_rarity != -1:
            #         cost_total += min_rarity

            # return cost_total

            # Previous version
            cost_total = 0
            for index in range(len(state_split)):
                if state_split[index] != goal_split[index]:
                    cost_total += 1 # for each move we have to make and each frequency will be at least one so admissible
            return cost_total


        return
