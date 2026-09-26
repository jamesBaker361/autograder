from dc import DC
from search import uniform_cost_search, astar_search

words = [('why', 'ask'), ( 'bear', 'duck')]
search= ['steps', 'scrabble', 'frequency']

for initial,goal in words:
    for cost in search:
        print(initial + ", " + goal + ", " + cost)

        problem_u = DC(initial, goal, cost)
        solution_u = uniform_cost_search(problem_u, display=True)
        print(f"Uniform search: {solution_u.path_cost}")

        problem_a = DC(initial, goal, cost)
        solution_a = astar_search(problem_a, display=True)
        print(f"A* search: {solution_a.path_cost}\n\n")