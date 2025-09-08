import sys
import itertools
from functools import cache
from random import choices


COLORS = 'BGKRWY'  # Blue, Green, blacK, Red, White, Yellow
SECRET = None

@cache
def score(a, b):
    matches = sum(x == y for x, y in zip(a, b))
    return matches, sum(min(a.count(c), b.count(c)) for c in COLORS) - matches

allcodes = tuple(''.join(p) for p in itertools.product(COLORS, repeat=4))
responses = [(matches, ncolors) for matches in range(5)
             for ncolors in range(5 - matches)]
responses.remove((3, 1))  # +++- cannot be a valid response

def add_info(g, S, symbol=False):
    if len(S) == 0:  # answers have been inconsistent
        return ["inconsistent", "#"][symbol]
    if len(S) == 1:  # the final correct answer
        return ["final", "!"][symbol]
    if g in S:       # possibly the correct answer
        return ["possible", "?"][symbol]
    else:            # definitely not the correct answer yet
        return ["impossible", "*"][symbol]

def get_response(g, S):
    if SECRET:
        return score(SECRET, g)

    inp = input('%s %s: ' % (add_info(g, S), g))
    if set(inp) - set('+-'):
        sys.exit("ill-formed response: %r" % inp)
    resp = inp.count('+'), inp.count('-')
    if resp not in responses:
        sys.exit("invalid response: %r" % inp)
    return resp

@cache
def guess(S):
    if len(S) == len(allcodes):  # first
        return 'BBGG'
    if len(S) == 1:
        return S[0]
    # Pick a guess which minimizes the maximum number of remaining S over
    # all 14 responses.
    # The guess will result in the minimum elements S remaining in the
    # next step, regardless of what the next response actually is.
    return min(allcodes, key=lambda t: max(sum(score(s, t) == resp for s in S)
                                           for resp in responses))

def solve(verbose=True):
    S = allcodes
    for i in itertools.count(1):
        g = guess(S)
        resp = get_response(g, S)
        if verbose:
            print("%2d %4d %s %5s %s" %
                  (i, len(S), g, g in S, '+' * resp[0] + '-' * resp[1]))
        if resp == (4, 0) or not S:
            return i
        # only keep the codes which would give the same response
        S = tuple(s for s in S if score(s, g) == resp)

def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: %s [secret]" % sys.argv[0])

    if len(sys.argv) == 2:
        global SECRET
        SECRET = sys.argv[1]
        if SECRET == '-':
            SECRET = ''.join(choices(COLORS, k=4))
            print("secret: %s" % SECRET)
        if len(SECRET) != 4 or set(SECRET) - set(COLORS):
            sys.exit("ill-formed Mastermind code: %r" % SECRET)

    solve()

if __name__ == '__main__':
    main()
