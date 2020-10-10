import sys
import random
import itertools
from functools import lru_cache


COLORS = 'BGKRWY'  # Blue, Green, blacK, Red, White, Yellow
SECRET = None


@lru_cache(1 << 20)
def score(a, b):
    matches = sum(x == y for x, y in zip(a, b))
    return matches, sum(min(a.count(j), b.count(j)) for j in COLORS) - matches

possible = [''.join(p) for p in itertools.product(COLORS, repeat=4)]
results = [(right, wrong) for right in range(5) for wrong in range(5 - right)]
results.remove((3, 1))

cache = {}
def guess(S):
    if len(S) == len(possible):  # first
        return 'BBGG'
    if len(S) == 1:
        return list(S)[0]
    # From all possible guesses, pick the one which maximizes the worst
    # reduction in S.  That is, the one with minimum elements from S
    # being eliminated for all possible responses.
    return max(possible,
               key=lambda p: min(sum(score(s, p) != res for s in S)
                                 for res in results))

def solve():
    S = set(possible)
    for i in itertools.count(1):
        g = guess(S)
        if SECRET is None:
            inp = input("%s: " % g)
            resp = inp.count('+'), inp.count('-')
        else:
            resp = score(SECRET, g)
            print("%d %4d %s %s" % (i, len(S), g,
                                    '+' * resp[0] + '-' * resp[1]))
        if resp == (4, 0):
            return i
        # eliminate the codes which would not give the same response
        S -= set(s for s in S if score(s, g) != resp)

if __name__ == '__main__':
    if len(sys.argv) > 2:
        sys.exit("Usage: %s [secret]" % sys.argv[0])

    if len(sys.argv) == 2:
        SECRET = sys.argv[1]
        if SECRET == '-':
            SECRET = ''.join(random.choices(COLORS, k=4))
            print("secret: %s" % SECRET)
            solve()
            sys.exit()
        if len(SECRET) != 4 or set(SECRET) - set(COLORS):
            sys.exit("is not a well-formed Mastermind code: %r" % SECRET)

    solve()
