from mastermind import allcodes, guess, score


# map responses to guess
table = {}

def solve(secret):
    S = allcodes
    responses = ""
    resp = None

    while True:
        if resp:
            responses += "%d%d " % resp
        g = guess(S)

        value = g
        # Meaning of symbols:
        #   no symbol: definitely the correct answer
        #     '*'    : definitely not the correct answer yet
        #     '?'    : maybe the answer
        if len(S) > 1:
            value += '?' if g in S else '*'

        try:
            assert table[responses] == value
        except KeyError:
            table[responses] = value

        resp = score(g, secret)
        if resp == (4, 0):
            return

        S = tuple(s for s in S if score(s, g) == resp)

for secret in allcodes:
    solve(secret)

with open('table.txt', 'w') as fo:
    for responses in sorted(table):
        fo.write(responses + table[responses] + '\n')
