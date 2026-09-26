
""" 8-Puzzle solution adapted from one by Matt Dailey (June 2004)
http://www.siit.tu.ac.th/mdailey/class/2004_s1/its216/data/8puzzle.py.

usage: python3 p8.py

"""

import sys
import search        # AIMA module for search problems
import random
import time

default_goal = '*12345678'
#default_goal = '1238*4765'

class P8(search.Problem):
    """A state is represented as a 9-character string with digits 1-8
    for tiles and '*' for a blank."""
    name = 'NIL'

    def __init__(self, goal=default_goal, initial=None, N=10):
        self.goal = goal
        self.initial = initial if initial else random_state(goal, N)

    def goal_test(self, s):
        """ Returns True iff s is a goal """
        return s == self.goal

    def actions(self, s):
        return actions8(s)

    def result(self, S, A):
        return result8(S,A)

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2
        from state1 via action, assuming cost c to get up to
        state1. The addional cost of every action is 1. """
        return c + 1

    def h(self, node):
        """Null heuristic for 8 puzzle: returns 0 for a goal 1 otherwise """
        return 0 if node == self.goal else 1
    
def actions8(S):
    """ Returns list of action possible in state S """
    action_table = {
        0:['down', 'right'],
        1:['down', 'left', 'right'],
        2:['down', 'left'],
        3:['up','down','right'],
        4:['up','down','left','right'],
        5:['up','down','left'],
        6:['up','right'],
        7:['up','left','right'],
        8:['up','left']}
    return action_table[S.index('*')]

def result8(S, A):
    """ Returns 8puzzle state after doing action A in state S"""
    blank = S.index('*')  # blank position, swap is location we want to movie it to
    if A == 'up':
        swap = blank - 3
        return ''.join([S[0:swap], '*', S[swap+1:blank], S[swap], S[blank+1:]])
    elif A == 'down':
        swap = blank + 3
        return ''.join([S[0:blank], S[swap], S[blank+1:swap], '*', S[swap+1:]])
    elif A == 'left':
        swap = blank - 1
        return ''.join([S[0:swap], '*', S[swap], S[blank+1:]])
    elif A == 'right':
        swap = blank + 1
        return ''.join([S[0:blank], S[swap], '*', S[swap+1:]])
    raise ValueError('Unrecognized action: ' + A)


class P8_OOP(P8):
    """ Eight puzzle using a heuristic function that is the number of tiles out of place"""

    name = 'OOP'

    def h(self, node):
        """8 puzzle heuristic: number of tiles 'out of place'"""
        mismatches = 0
        for (t1,t2) in zip(node.state, self.goal):
            if  t1 != t2:
                mismatches += 1
        return mismatches

class P8_MHD(P8):
    name = 'MHD'

    def h(self, node):
        """8 Puzzle Heuristic: sum for each tile of manhattan distance
        between its position in node's state and goal """
        sum = 0
        for tile in '12345678':
            sum += mhd(node.state.index(tile), self.goal.index(tile))
        return sum

def mhd(n, m):
    """Returns manhattan-distance between two indices in a
       nine-character string corresponding to a 3x3 array"""
    # dict of x,y coordinates for each character position
    coordinates = {0:(0,0), 1:(1,0), 2:(2,0),
                   3:(0,1), 4:(1,1), 5:(2,1),
                   6:(0,2), 7:(1,2), 8:(2,2)}
    if n == m:
        return 0
    else:
        x1, y1 = coordinates[n]
        x2, y2 = coordinates[m]
        return abs(x1-x2) + abs(y1-y2)

def random_state(s, n, unique=True):
    """ Returns state reached after random walk of length n starting
    from s. If unique is True, each state on the walk must be unique,
    preventing loops"""

    return simple_random_state(s, n) if not unique else nodups_random_state(s, n)

def simple_random_state(s, n):
    """returns resulting state after a simple random walk of n steps
       starting with state s.  The result might contain loops. """
    for _ in range(n):
        s = result8(s, random.choice(actions8(s)))
    return s

def random_state(state, n):
    """returns result after a random walk of n steps w/o loops
       starting with state"""
    visited = set()
    for _ in range(n):
        actions =  list(actions8(state))
        random.shuffle(actions)
        for act in actions:
            next = result8(state, act)
            if next not in visited:
                break
        if next in visited: #should not happen
            print(f"Looping: {visited}")
        visited.add(next)
        state = next
    # return last state
    return state

def printsoln(goal):
    """shows solution to 8 puzzle"""
    # path is list of Nodes from initial to goal
    path = goal.path()
    print(f"{len(path)-1} steps from {path[0].state} to {goal.state}")
    for node in path:
        a = node.action
        s = node.state
        print("%s\t%s\n\t%s\n\t%s\n" % (a,s[0:3],s[3:6],s[6:9]))

def print_state(s):
     print(f"{s[0:3]}\n{s[3:6]}\n{s[6:9]}\n")

def solve(initial=None, n=10):
    """Solves a random 8 puzzle problem and prints info"""
    if initial:
        s = initial
        print(f"P8: {initial} => {default_goal}")
    else:
        s = random_state(default_goal, n)
        print(f"\n{s} => {default_goal} ({n} steps from start)")        
        print(f"heur.\tsteps\tdepth\tstates\tsuccs\tEBF\tseconds")        
    
    for p in [P8(initial=s), P8_OOP(initial=s), P8_MHD(initial=s)]:
        solve1(p, n=n)

def solve1(p, n=10):
    ip = search.InstrumentedProblem(p)
    begin_time = time.time()
    solution = search.astar_search(ip)
    elapsed = time.time() - begin_time
    if solution:
        depth = len(solution.path())-1
        eb = ebf(ip.succs, depth)
        print(f"{p.name}\t{n}\t{depth}\t{ip.states}\t{ip.succs}\t{eb:.2f}\t{elapsed:.5f}")
        return solution
    else:
        print("  No solution found ☹")

def ebf(n, d):
    """ returns an estimate of the effective branching factor, which is the number
    of successors generated by a "typical" node for a given search problem.
      n: states whose successors have been generated.
      d: depth at which the solution node was found
      b: effective branching factor
      N = b + (b)**2 + ... + (b)**d
    There is no closed form solution to computing it, but this gives  a rough estimate"""
    
    return n ** (1/d)

            
def run_problems(steps=[5,10,15,18]):
    """ Solve an instance of the 8 puzzle from an inital state reached
    by a random walk of N steps for each N in the list steps"""
    for nsteps in steps:
        solve(n=nsteps)

# if called from the command line, call main()
# e.g., python py8.py 10 20 30
if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_problems([int(arg) for arg in sys.argv[1:]])
    else:
        run_problems()
        
