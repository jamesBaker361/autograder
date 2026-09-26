""" Find the lowest cost way to transform a three or four letter word into another by changing one
letter at a time so that all of the intervening strings are legal English words. The cost of a
replacement letter can be 1 (steps), based on scrabble values (scrabble), or based on the resulting
words frequency in normal text (frequency) """

import argparse
import time

from dc import DC, dictionary
from search import astar_search

usage = """
usage: python dcsolve.py word1 word2 [steps|scrabble|frequency]
  e.g. python dcsolve.py hat pin steps
"""

def dcsolver(initial="dog", goal="cat", cost='steps'):
    """ solve a dog-cat problem, print the solution, it's cost the the time taken """
    problem = DC(initial, goal, cost)
    start = time.time()
    solution = astar_search(problem)
    elapsed = time.time() - start
    if  solution:
        solution_path = path = ' '.join([node.state for node in solution.path()])
        solution_cost = solution.path_cost
        # show how much h() underestimated H-star. Should all be <= 0
        deltas = [rnd(node.path_cost + problem.h(node) - solution_cost) for node in solution.path()][:-1]
    else:
        solution_path = "NO SOLUTION"
        deltas = []
        solution_cost = -1
    print(f"{problem} cost:{solution_cost:.2f}; time:{elapsed:.3f}; solution:{solution_path}; deltas:{deltas}")

def rnd(n):
    # round to 3 decimal places, replace -0.0 with 0.0
    n = round(n,3)
    return 0.0 if n == -0.0 else n     # -0.0 ==> 0.0

# if called from the command line, call dcsolver
if __name__ == "__main__":
    p = argparse.ArgumentParser(description='solve dogcat prolems with several cost functions')
    p.add_argument('word1', type=str, help='initial word')
    p.add_argument('word2', type=str, help='goal word')
    p.add_argument('cost', type=str, nargs="?", default="steps", choices=["steps","scrabble","frequency"], help="cost metric")
    args = p.parse_args()
    dcsolver(args.word1, args.word2, args.cost)
        

