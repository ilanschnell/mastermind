import sys
import random
import itertools
from functools import lru_cache

import mastermind
from mastermind import COLORS, get_response, score, possible, responses


def guess(S):
    if len(S) == len(possible):  # first
        res = 2 * random.sample(COLORS, 2)
        random.shuffle(res)
        return ''.join(res)
    if len(S) == 1:
        return list(S)[0]
    # Pick a guess which minimizes the maximum number of remaining S over
    # all 14 responses.
    # The guess will result in the minimum elements S remaining, in the
    # next step, regardless of what the next response is.
    worst = [max(sum(score(s, possible[i]) == resp for s in S)
                 for resp in responses)
             for i in range(1296)]
    minimum = min(worst)
    print('minimum:', minimum)
    choices = [possible[i] for i in range(1296) if worst[i] == minimum]
    print('choices:', len(choices))
    return random.choice(choices)

def solve():
    S = set(possible)
    for i in itertools.count(1):
        print("===== guess: %d    len(S): %s  =====" % (i, len(S)))
        g = guess(S)
        resp = get_response(g)
        print("%s %s" % (g, '+' * resp[0] + '-' * resp[1]))
        if resp == (4, 0):
            return i
        # only keep the codes which would give the same response
        S = set(s for s in S if score(s, g) == resp)

if __name__ == '__main__':
    if len(sys.argv) > 2:
        sys.exit("Usage: %s [secret]" % sys.argv[0])

    if len(sys.argv) == 2:
        mastermind.SECRET = sys.argv[1]
        if mastermind.SECRET == '-':
            mastermind.SECRET = ''.join(random.choices(COLORS, k=4))
            print("secret: %s" % mastermind.SECRET)
            solve()
            sys.exit()
        if len(mastermind.SECRET) != 4 or set(mastermind.SECRET) - set(COLORS):
            sys.exit("is not a well-formed Mastermind code: %r" %
                     mastermind.SECRET)

    solve()
