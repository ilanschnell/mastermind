import sys
import random
import itertools
from functools import lru_cache


COLORS = 'BGKRWY'  # Blue, Green, blacK, Red, White, Yellow
SECRET = None

@lru_cache(1 << 20)
def score(a, b):
    matches = sum(x == y for x, y in zip(a, b))
    return matches, sum(min(a.count(c), b.count(c)) for c in COLORS) - matches

possible = tuple(''.join(p) for p in itertools.product(COLORS, repeat=4))
responses = [(right, wrong) for right in range(5)
             for wrong in range(5 - right)]
responses.remove((3, 1))
assert len(responses) == 14

def get_response(g):
    if SECRET is None:
        inp = input("%s: " % g)
        return inp.count('+'), inp.count('-')
    return score(SECRET, g)

@lru_cache(1 << 10)
def guess(S):
    if len(S) == len(possible):  # first
        return 'BBGG'
    if len(S) == 1:
        return S[0]
    # Pick a guess which minimizes the maximum number of remaining S over
    # all 14 responses.
    # The guess will result in the minimum elements S remaining, in the
    # next step, regardless of what the next response is.
    return min(possible, key=lambda p: max(sum(score(s, p) == resp for s in S)
                                           for resp in responses))

def solve():
    S = possible
    for i in itertools.count(1):
        g = guess(S)
        resp = get_response(g)
        print("%d %4d %s %s" % (i, len(S), g, '+' * resp[0] + '-' * resp[1]))
        if resp == (4, 0):
            return i
        # only keep the codes which would give the same response
        S = tuple(s for s in S if score(s, g) == resp)

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
