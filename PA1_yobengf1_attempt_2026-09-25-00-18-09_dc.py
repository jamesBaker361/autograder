import search
import gzip

dict_file = "words34.txt.gz"

dictionary = {}

for line in gzip.open(dict_file, 'rt'):
    word, n = line.strip().split('\t')
    n = float(n)
    dictionary[word] = n


scrabble_values = {
    'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1,
    'l': 1, 'n': 1, 's': 1, 't': 1, 'r': 1,
    'd': 2, 'g': 2,
    'b': 3, 'c': 3, 'm': 3, 'p': 3,
    'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4,
    'k': 5,
    'j': 6, 'x': 6,
    'q': 10, 'z': 10
}


class DC(search.Problem):

    def __init__(self, initial='dog', goal='cat', cost='steps'):

        if not isinstance(initial, str) or not isinstance(goal, str):
            raise ValueError("Initial and goal must be strings")

        if initial != initial.lower() or goal != goal.lower():
            raise ValueError("Initial and goal must be lowercase")

        if not initial.isalpha() or not goal.isalpha():
            raise ValueError("Initial and goal must contain only letters")

        if len(initial) not in (3, 4) or len(goal) not in (3, 4):
            raise ValueError("Words must contain three or four letters")

        if len(initial) != len(goal):
            raise ValueError("Initial and goal must have the same length")

        if initial not in dictionary:
            raise ValueError("Initial word is not in the dictionary")

        if goal not in dictionary:
            raise ValueError("Goal word is not in the dictionary")

        if cost not in ('steps', 'scrabble', 'frequency'):
            raise ValueError(
                "Cost must be 'steps', 'scrabble', or 'frequency'"
            )

        super().__init__(initial, goal)

        self.cost = cost


    def actions(self, state):

        possible_actions = []

        for position in range(len(state)):

            for letter in 'abcdefghijklmnopqrstuvwxyz':

                if letter == state[position]:
                    continue

                new_word = (
                    state[:position]
                    + letter
                    + state[position + 1:]
                )

                if new_word in dictionary:
                    possible_actions.append((position, letter))

        return possible_actions


    def result(self, state, action):

        position, letter = action

        return (
            state[:position]
            + letter
            + state[position + 1:]
        )


    def goal_test(self, state):

        return state == self.goal


    def path_cost(self, c, state1, action, state2):

        if self.cost == 'steps':
            return c + 1

        elif self.cost == 'scrabble':
            position, new_letter = action
            return c + scrabble_values[new_letter]

        elif self.cost == 'frequency':
            return c + 1 + dictionary[state2]


    def __repr__(self):

        return f"dc({self.initial},{self.goal},{self.cost})"


    def h(self, node):

        state = node.state

        if state == self.goal:
            return 0

        different_positions = [
            i
            for i in range(len(state))
            if state[i] != self.goal[i]
        ]

        if self.cost == 'steps':
            return len(different_positions)

        elif self.cost == 'scrabble':

            estimate = 0

            for position in different_positions:
                goal_letter = self.goal[position]
                estimate += scrabble_values[goal_letter]

            return estimate

        elif self.cost == 'frequency':
            return len(different_positions)