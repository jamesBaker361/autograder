from dc import DC
from search import astar_search, uniform_cost_search

cases = [ ("why", "ask"), ("bear", "duck")]

costs = ["steps", "scrabble", "frequency"]

for initial, goal in cases:
    for cost in costs:
        print(f"\n{initial} -> {goal}, cost={cost}")

        ucs = DC(initial, goal, cost)
        print("UCS:")
        ucs_result = uniform_cost_search(ucs, display=True)
        print("Solution cost:", ucs_result.path_cost)

        astar = DC(initial, goal, cost)
        print("A*:")
        astar_result = astar_search(astar, display=True)
        print("Solution cost:", astar_result.path_cost)