from dc import DC
from search import uniform_cost_search, astar_search

words = [('why', 'ask'), ( 'bear', 'duck')]

for initial,goal in words:
    print(initial + ", " + goal)

    problem_h0_a = DC(initial, goal, "frequency")
    solution_h0_a = astar_search(problem_h0_a, h=problem_h0_a.h, display=True)
    print(f"H0 A*: {solution_h0_a.path_cost}")

    problem_h1_a = DC(initial, goal, "frequency")
    solution_h1_a = astar_search(problem_h1_a, h=problem_h1_a.h_goal_rarity, display=True)
    print(f"H1 A*: {solution_h1_a.path_cost}\n\n")