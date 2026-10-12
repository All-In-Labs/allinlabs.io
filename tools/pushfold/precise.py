# Precise big-blind call EV for borderline hands when the small blind shoves any two cards
# (the 10bb equal-stack bubble). Constants are that setup's ICM values from solve.py.
# Usage: python precise.py KJo QJs A9o
import random, sys, eval7
from multiprocessing import Pool
from equities import rep, RANKS, SUITS
WIN, TIE, FOLD = 0.38333333, 0.25, 0.23343920145190564
deck=[r+s for r in RANKS for s in SUITS]
def run(h):
    hc=[eval7.Card(x) for x in rep(h)]
    rest=[x for x in deck if x not in rep(h)]
    vill=','.join(a+b for i,a in enumerate(rest) for b in rest[i+1:])
    eq=eval7.py_hand_vs_range_monte_carlo(hc, eval7.HandRange(vill), [], 20000000)
    rnd=random.Random(h); rc=[eval7.Card(x) for x in rest]; ties=0; n=400000
    for _ in range(n):
        s=rnd.sample(rc,7)
        if eval7.evaluate(hc+s[2:])==eval7.evaluate(s): ties+=1
    t=ties/n; w=eq-t/2
    return h, eq, t, w*WIN+t*TIE-FOLD
if __name__=='__main__':
    with Pool() as p:
        for h,eq,t,g in p.map(run, sys.argv[1:]):
            print(f'{h:4} eq {eq:.4f} tie {t:.4f} gain {g:+.5f} -> {"call" if g>0 else "fold"}')
