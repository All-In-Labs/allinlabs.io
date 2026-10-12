# Small blind push/fold equilibrium against the big blind, 4 players left, everyone on S big blinds.
# Valued in chips (cev) or with ICM (Malmuth-Harville) over the payouts. Fictitious play.
import itertools, json, sys
import numpy as np
from equities import classes

mode, S = sys.argv[1], float(sys.argv[2])
PAY = [0.5, 0.3, 0.2, 0.0]
eq = json.load(open('eq.json'))
cs = classes(); N = len(cs)

def icm(stacks):
    """Expected payout of each player (Malmuth-Harville)."""
    n = len(stacks); out = [0.0] * n
    def rec(remaining, prob, place):
        tot = sum(stacks[i] for i in remaining)
        for i in remaining:
            if stacks[i] <= 0: continue
            p = prob * stacks[i] / tot
            out[i] += p * PAY[place]
            rest = [j for j in remaining if j != i]
            if rest and place + 1 < len(PAY): rec(rest, p, place + 1)
    alive = [i for i in range(n) if stacks[i] > 0]
    rec(alive, 1.0, 0)
    return out

def value(sb, bb):  # (SB value, BB value) for the resulting stacks; others keep S
    if mode == 'cev': return sb, bb
    v = icm([sb, bb, S, S]); return v[0], v[1]

FOLD = value(S - 0.5, S + 0.5)
STEAL = value(S + 1, S - 1)
WIN = value(2 * S, 0)      # SB wins the all in
LOSE = value(0, 2 * S)
TIE = value(S, S)

n = np.zeros((N, N)); E = np.zeros((N, N)); T = np.zeros((N, N))
for i, h in enumerate(cs):
    for j, g in enumerate(cs):
        d = eq[f'{h}|{g}']; n[i, j] = d['n']
        if d['n']: E[i, j] = d['eq']; T[i, j] = d['tie']
W = E - T / 2; L = 1 - E - T / 2           # SB's win/lose probability, hand i vs hand j
combos = np.array([6 if len(c) == 2 else 4 if c[2] == 's' else 12 for c in cs], float)

# SB: push value per hand given BB's call strategy c (prob BB holds j given SB holds i ~ n[i,j]).
called_sb = W * WIN[0] + T * TIE[0] + L * LOSE[0]
called_bb = W * WIN[1] + T * TIE[1] + L * LOSE[1]   # BB's value when SB holds i, BB holds j

def sb_push_ev(c):
    return (n * (c * called_sb + (1 - c) * STEAL[0])).sum(1) / n.sum(1)

def bb_call_gain(p):
    # BB holds j; SB's hand i weighted by its combos compatible with j, times SB's push prob.
    w = n * p            # w[j,i]: SB combos of class i compatible with BB's hand j, times push prob
    call = (w * called_bb.T).sum(1); fold = w.sum(1) * STEAL[1]
    return np.where(w.sum(1) > 0, (call - fold) / np.maximum(w.sum(1), 1e-12), -1)

p = np.ones(N); c = np.zeros(N); P = np.zeros(N); C = np.zeros(N)
for t in range(1, 5001):
    c_br = (bb_call_gain(p) > 0).astype(float)
    p_br = (sb_push_ev(c) > FOLD[0]).astype(float)
    C += c_br; P += p_br; c = C / t; p = P / t

push_margin = sb_push_ev(c) - FOLD[0]
call_margin = bb_call_gain(p)
pct = lambda x: 100 * (combos * x).sum() / 1326
print(f'{mode} {S}bb: SB pushes {pct(p > 0.5):.1f}%, BB calls {pct(c > 0.5):.1f}%')
mixed = [(cs[i], round(p[i], 2)) for i in range(N) if 0.02 < p[i] < 0.98]
print('mixed SB hands:', mixed)
print('mixed BB hands:', [(cs[i], round(c[i], 2)) for i in range(N) if 0.02 < c[i] < 0.98])
# closest-to-indifferent pushes, in units of prize pool (or chips)
order = np.argsort(np.abs(push_margin))[:8]
print('closest SB decisions:', [(cs[i], f'{push_margin[i]:+.5f}') for i in order])
json.dump({'push': p.tolist(), 'call': c.tolist()}, open(f'sol_{mode}_{int(S)}.json', 'w'))

print('    ' + '   '.join(RANK for RANK in 'AKQJT98765432'))
for r in range(13):
    row = 'AKQJT98765432'[r] + '   '
    for k in range(13):
        i = r * 13 + k
        row += ((cs[i] if p[i] > 0.5 else '·') + '    ')[:4]
    print(row.rstrip())
