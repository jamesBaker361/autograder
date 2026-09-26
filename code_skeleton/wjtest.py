import sys
import argparse
import wj
import search as s

# default searchers from aima.search to use
default_searchers = [s.breadth_first_tree_search,
                     s.breadth_first_graph_search,
                     s.depth_first_graph_search,
                     s.iterative_deepening_search,
                     s.astar_search]

def wjsolve(capacities, start, goal, searchers=default_searchers):
    problem = wj.WJ(capacities, start, goal)
    print("Solving {}".format(problem))
    for alg in searchers:
        print('\n\nSearch algorithm:', alg.__name__)
        wj.print_solution(alg(problem))

    print("\n\nSUMMARY: successors/goal tests/states generated/solution\n")
    #s.compare_searchers([wj2.WJ2(capacities, start, goal)], [], searchers)
    s.compare_searchers([problem], [], searchers)

def convert(g1_g2):
    """ Returns tuple (g1,g2) after converting g1 and g2 to integers
    unless they are  """
    g1, g2 = (g1_g2)
    return (int(g1), int(g2))


# if called from the command line, call wjsolve
if __name__ == "__main__":
    p = argparse.ArgumentParser(description='Test wj problem with several search algorithms')
    p.add_argument ('-c', '--capacities', nargs=2, type=int, default=[9,4])
    p.add_argument ('-i', '--initial', nargs=2, type=int, default=[9,4])
    p.add_argument ('-g', '--goal', nargs=2, type=int, default=[-1,1])
    args = p.parse_args()
    wjsolve(tuple(args.capacities), tuple(args.initial), tuple(args.goal))
        

