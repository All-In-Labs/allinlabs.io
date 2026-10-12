# Win/tie/lose probabilities for every pair of the 169 starting-hand classes, all in preflop.
# Equity (ties as half) from eval7's C Monte Carlo; tie rate from a separate sampled estimate.
import itertools, json, random, sys
from multiprocessing import Pool
import eval7

RANKS = 'AKQJT98765432'
SUITS = 'shdc'

def classes():
    out = []
    for i, a in enumerate(RANKS):
        for j, b in enumerate(RANKS):
            if i == j: out.append(a + b)
            elif i < j: out.append(a + b + 's')
            else: out.append(b + a + 'o')
    return out  # row-major 13x13: suited above the diagonal, offsuit below

def combos(c):
    a, b = c[0], c[1]
    if len(c) == 2:
        return [(a + s1, b + s2) for s1, s2 in itertools.combinations(SUITS, 2)]
    if c[2] == 's':
        return [(a + s, b + s) for s in SUITS]
    return [(a + s1, b + s2) for s1 in SUITS for s2 in SUITS if s1 != s2]

# One representative combo per class is exact against a whole class: every combo of a class maps
# to every other under a suit permutation, which leaves the opposing class unchanged.
def rep(c): return combos(c)[0]

def work(pair):
    h, g, iters, tie_samples, seed = pair
    rnd = random.Random(seed)
    hc = [eval7.Card(x) for x in rep(h)]
    used = set(rep(h))
    vs = [v for v in combos(g) if not (set(v) & used)]
    if not vs: return (h, g, 0, None, None)
    eq = eval7.py_hand_vs_range_monte_carlo(hc, eval7.HandRange(','.join(a + b for a, b in vs)), [], iters)
    deck_all = [r + s for r in RANKS for s in SUITS]
    ties = 0
    for _ in range(tie_samples):
        v = rnd.choice(vs)
        rest = [x for x in deck_all if x not in used and x not in v]
        board = [eval7.Card(x) for x in rnd.sample(rest, 5)]
        vc = [eval7.Card(x) for x in v]
        if eval7.evaluate(hc + board) == eval7.evaluate(vc + board): ties += 1
    return (h, g, len(vs), eq, ties / tie_samples)

if __name__ == '__main__':
    iters, tie_samples = int(sys.argv[1]), int(sys.argv[2])
    cs = classes()
    jobs = [(h, g, iters, tie_samples, k) for k, (h, g) in enumerate(itertools.product(cs, cs))]
    with Pool() as p:
        res = p.map(work, jobs, chunksize=64)
    out = {f'{h}|{g}': {'n': n, 'eq': eq, 'tie': t} for h, g, n, eq, t in res}
    json.dump(out, open(sys.argv[3], 'w'))
    print(len(out), 'pairs')
