import sys
from collections import defaultdict

import mastermind


def test_score():
    for a, b, r in [
            ('BBKB', 'BBGG', (2, 0)),
            ('BGKR', 'BGKR', (4, 0)),
            ('YBRK', 'BBGW', (1, 0)),
            ('BBKB', 'BGKR', (2, 0)),
            ('BGKB', 'KBGB', (1, 3)),
            ('BGKR', 'GKRB', (0, 4)),
            ('GBKR', 'BGKR', (2, 2)),
            ('BGGG', 'KRKR', (0, 0)),
            ('BBKK', 'BKGG', (1, 1)),
            ('BBKY', 'BKGY', (2, 1)),
            ('GGBB', 'BBGG', (0, 4)),
    ]:
        assert mastermind.score(a, b) == mastermind.score(b, a) == r

def test_all():
    stat = defaultdict(int)
    for secret in mastermind.possible:
        mastermind.SECRET = secret
        print("secret: %s" % secret)
        stat[mastermind.solve()] += 1
    print(stat)
    n = sum(i * n for i, n in stat.items())
    print('n:', n)
    print('average: %.2f' % (n / len(mastermind.possible)))
    print('worst: %d' % max(stat.keys()))
    #print('cache:', len(cache))
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
