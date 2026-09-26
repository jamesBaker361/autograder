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

    # Store replacement-letter costs in one lookup table.
    SCRABBLE_VALUES = {  
        **dict.fromkeys("aeioulnstr", 1),  # These common letters each cost 1 point.
        **dict.fromkeys("dg", 2),  # D and G each cost 2 points.
        **dict.fromkeys("bcmp", 3),  # B, C, M, and P each cost 3 points.
        **dict.fromkeys("fhvwy", 4),  # F, H, V, W, and Y each cost 4 points.
        "k": 5,  # K costs 5 points.
        **dict.fromkeys("jx", 6),  # J and X each cost 6 points.
        **dict.fromkeys("qz", 10),  # Q and Z each cost 10 points.
    }  

    # Cache the smallest rarity because the frequency heuristic uses it often.
    MIN_RARITY = min(dictionary.values())  
    
    # -------------------------------------------------------------------------
    # Function: __init__
    # Purpose: Set up one DOGCAT problem and reject bad input before searching.
    # Parameters:
    #   initial (str): Starting 3- or 4-letter lowercase dictionary word.
    #   goal (str): Target word. Must be the same length as initial.
    #   cost (str): Cost rule: 'steps', 'scrabble', or 'frequency'.
    # Returns: Nothing. The settings are stored in this DC object.
    # -------------------------------------------------------------------------
    def __init__(self, initial='dog', goal='cat', cost='steps'):  # Build one DOGCAT problem instance from its start, goal, and cost rule.
        """Store the problem settings and reject invalid arguments early."""  # Explain the constructor's main job.
        valid_costs = {'steps', 'scrabble', 'frequency'}  # List the only cost names accepted by PA1.

        if not isinstance(initial, str) or not isinstance(goal, str):  # Make sure both states are actually strings before checking them further.
            raise ValueError('initial and goal must be strings')  # Stop early if either state has the wrong data type.
        
        if initial != initial.lower() or goal != goal.lower():  # PA1 only allows lowercase word states.
            raise ValueError('initial and goal must be lowercase')  # Reject mixed-case or uppercase input clearly.
        
        if len(initial) not in (3, 4) or len(goal) not in (3, 4):  # DOGCAT states must be exactly three or four letters long.
            raise ValueError('initial and goal must have three or four letters')  # Reject words outside the allowed lengths.
        
        if len(initial) != len(goal):  # A one-letter replacement never changes word length, so both ends must match.
            raise ValueError('initial and goal must have the same length')  # Reject an impossible start/goal length pairing.
        
        if initial not in dictionary or goal not in dictionary:  # Both endpoint words must be legal words from the supplied file.
            raise ValueError('initial and goal must appear in the supplied dictionary')  # Reject words the search graph does not contain.
        
        if not isinstance(cost, str) or cost not in valid_costs:  # Check that the selected cost rule is one the program knows.
            raise ValueError("cost must be 'steps', 'scrabble', or 'frequency'")  # Give a useful message instead of failing later in the search.

        super().__init__(initial, goal)  # Let AIMA's Problem class store the initial and goal states in its standard fields.
        self.cost = cost  # Save the chosen cost rule so path_cost() and h() can use the same setting.

    # -------------------------------------------------------------------------
    # Function: actions
    # Purpose: Find every legal one-letter replacement from the current word.
    # Parameters:
    #   state (str): Current legal 3- or 4-letter word.
    # Returns: A list of (position, replacement_letter) action tuples.
    # -------------------------------------------------------------------------
    def actions(self, state):  # Find every legal one-letter move available from the current word.
        """ Given a state (i.e., a word), return a list or iterator of
                all possible next actions.  An action is defined by position
                in the word and a character to put in that position.  But the
                result must be a legal word, i.e., in our dictionary, and it
                should not be the same as the state, i.e., don't replace a
                character with the same character """
                
        legal = []  # Collect legal actions here and return the finished list at the end.
        
        for pos, old_char in enumerate(state):  # Visit each character position and remember the letter currently there.
            
            for new_char in 'abcdefghijklmnopqrstuvwxyz':  # Try every lowercase letter as a possible replacement at this position.
                
                if new_char == old_char:  # Replacing a letter with itself would leave the state unchanged.
                    continue  # Skip that no-op and move on to the next candidate letter.
                
                candidate = state[:pos] + new_char + state[pos + 1:]  # Build the word produced by this one-letter replacement.
                
                if candidate in dictionary:  # Only dictionary words count as legal successor states.
                    legal.append((pos, new_char))  # Save the legal move as the required (position, new_letter) action tuple.
        
        return legal  # Give AIMA every legal successor action from this state.

    # -------------------------------------------------------------------------
    # Function: result
    # Purpose: Apply one legal replacement action and build the next word.
    # Parameters:
    #   state (str): Current word before the move.
    #   action (tuple): (position, replacement_letter) to apply.
    # Returns: The new word produced by that one-letter change.
    # -------------------------------------------------------------------------
    def result(self, state, action):  # Apply one action and return the word that action creates.
        """ takes a state and an action and returns a new state """
        pos, new_char = action  # Unpack the action into the index to change and the letter to insert.
        return state[:pos] + new_char + state[pos + 1:]  # Replace exactly one character while preserving the rest of the word.

    # -------------------------------------------------------------------------
    # Function: goal_test
    # Purpose: Tell the search code whether the current word is the goal.
    # Parameters:
    #   state (str): Current word being checked.
    # Returns: True if state equals the goal word; otherwise False.
    # -------------------------------------------------------------------------
    def goal_test(self, state):  # Check whether the search has reached the requested destination word.
        """ returns True iff state is a goal state for this problem instance """
        
        return state == self.goal  # True means this state is the goal; False means the search should keep going.

    # -------------------------------------------------------------------------
    # Function: path_cost
    # Purpose: Add one move's cost to the total path cost built so far.
    # Parameters:
    #   c (number): Cost already paid to reach state1.
    #   state1 (str): Word before the move.
    #   action (tuple): (position, replacement_letter) used for the move.
    #   state2 (str): Word produced by the move.
    # Returns: Updated cumulative path cost using the selected cost rule.
    # -------------------------------------------------------------------------
    def path_cost(self, c, state1, action, state2):  # Add the cost of one transition to the path cost accumulated so far.
        """ Returns the cost to get to state2 by applying action in
                state1 given that c is the cost to get up to state1. For the 
                the dc problem, you will have to check what
                cost metric (self.cost) is being used for this problem instance,
                i.e., is it steps, scrabble or frequency """
                
        if self.cost == 'steps':  # Under the steps metric, every legal move has the same cost.
            return c + 1  # Add exactly one for this replacement.
        
        if self.cost == 'scrabble':  # Under Scrabble cost, only the newly inserted letter determines this move's cost.
            _, new_char = action  # We only need the replacement letter, so ignore the position with an underscore.
            return c + self.SCRABBLE_VALUES[new_char]  # Add PA1's Scrabble value for that inserted letter.
        
        # Frequency cost is charged for the word produced by the action.
        return c + 1 + dictionary[state2]  # Add the base cost of 1 plus the rarity of the resulting word.


    # -------------------------------------------------------------------------
    # Function: __repr__
    # Purpose: Give the problem a short readable label for output and debugging.
    # Parameters: None beyond this DC object.
    # Returns: A string showing initial word, goal word, and cost rule.
    # -------------------------------------------------------------------------
    def __repr__(self):  # Provide a short text form that is useful in solver output and debugging.
        """" return a suitable string to represent this problem instance """
        return f"dc({self.initial},{self.goal},{self.cost})"  # Show the start word, goal word, and active cost rule together.

    # -------------------------------------------------------------------------
    # Function: h
    # Purpose: Estimate the minimum remaining cost for A* without overestimating.
    # Parameters:
    #   node (search.Node): Search node whose state is the current word.
    # Returns: A nonnegative heuristic estimate based on the active cost rule.
    # -------------------------------------------------------------------------
    def h(self, node):  # Estimate the cheapest remaining cost from this search node to the goal.
        """Heuristic: returns an estimate of the cost to get from the
                state of the node to the goal state. The heuristic's value should
                depend on the Problem's cost parameter, self.cost (i.e., steps, scrabble
                or frequency), as this will effect the estimate cost to get to
                the nearest goal. """
        
        state = node.state  # Pull the word out of the AIMA Node object for easier use below.
        mismatches = [i for i, (a, b) in enumerate(zip(state, self.goal)) if a != b]  # Record every position whose current letter differs from the goal letter.
        d = len(mismatches)  # Count those mismatches; at least this many letter changes are still required.

        if d == 0:  # No mismatches means the current word already equals the goal.
            return 0  # A goal state has no remaining cost.

        if self.cost == 'steps':  # Use a Hamming-distance lower bound when each move costs exactly one.
            # Every action fixes at most one currently mismatched position.
            return d  # At least one action is needed for each mismatched character position.

        if self.cost == 'scrabble':  # Use the unavoidable goal-letter costs for the Scrabble metric.
            # Every mismatched position must eventually receive its goal letter.
            return sum(self.SCRABBLE_VALUES[self.goal[i]] for i in mismatches)  # Add the minimum required insertion cost for each mismatched goal position.

        # At least d actions remain. The final action must enter the goal,
        # while every earlier action costs at least 1 + the smallest rarity.
        return (d - 1) * (1 + self.MIN_RARITY) + (1 + dictionary[self.goal])  # Lower-bound earlier moves, then add the unavoidable cost of entering the goal.
