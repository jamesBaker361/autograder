from dc import DC, dictionary
from search import astar_search

rmin = min(dictionary.values())
print("r =", rmin)

class DC1(DC):
    def h(self, node):
        s = node.state
        wrong = sum(1 for a, b in zip(s, self.goal) if a != b)
        return wrong

class DC2(DC):
    def h(self, node):
        s = node.state
        wrong = sum(1 for a, b in zip(s, self.goal) if a != b)
        return wrong + rmin

pairs = [("why", "ask"), ("bear", "duck")]

for w1, w2 in pairs:
    print(f"\n{w1} -> {w2}, cost=frequency")

    print("Baseline h0:")
    p1 = DC1(w1, w2, "frequency")
    r1 = astar_search(p1, display=True)
    print("Solution cost:", r1.path_cost)

    print("Rarity-aware h_R:")
    p2 = DC2(w1, w2, "frequency")
    r2 = astar_search(p2, display=True)
    print("Solution cost:", r2.path_cost)