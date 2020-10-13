import re
import sys
import itertools
from collections import defaultdict

import mastermind
from mastermind import score, responses


mastermind.COLORS = '123456'

DATA = """\
1131 1122 20
1234 1234 40
6143 1125 10
1131 1234 20
1231 3121 13
1234 2341 04
2134 1234 22
1222 3434 00
1133 1322 11
1136 1326 21
2211 1122 04
"""

def test_score():
    pat = re.compile(r'(\d{4})\s+(\d{4})\s+(\d{2})')
    for line in DATA.splitlines():
        line = line.strip()
        m = pat.match(line)
        a = m.group(1)
        b = m.group(2)
        r = tuple([int(s) for s in m.group(3)])
        assert score(a, b) == score(b, a) == r

possible = [''.join(p) for p in itertools.product(mastermind.COLORS, repeat=4)]

cache = {}
def guess(S):
    if len(S) == len(possible):  # first
        return '1122'
    if len(S) == 1:
        return S[0]
    k = tuple(S)
    if k not in cache:
        cache[k] = min(possible,
                       key=lambda p: max(sum(score(s, p) == resp for s in S)
                                         for resp in responses))
    return cache[k]

def solve(secret):
    S = list(possible)
    guesses = set()
    for i in itertools.count(1):
        g = guess(S)
        assert g not in guesses
        guesses.add(g)
        resp = score(secret, g)
        print("%d %4d %s %s" % (i, len(S), g, '+' * resp[0] + '-' * resp[1]))
        if resp == (4, 0):
            return i
        S = [s for s in S if score(s, g) == resp]

def test_all():
    stat = defaultdict(int)
    for secret in possible:
        print("secret: %s" % secret)
        stat[solve(secret)] += 1
    print(stat)
    n = sum(i * n for i, n in stat.items())
    print('n:', n)
    print('average: %.2f' % (n / len(possible)))
    print('worst: %d' % max(stat.keys()))
    print('cache:', len(cache))
    assert stat == {
        1:    1,
        2:    6,
        3:   25,
        4:  239,
        5: 1025,
    }

if __name__ == '__main__':
    test_score()
    if len(sys.argv) > 1:
        test_all()
