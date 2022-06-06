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

        try:
            assert table[responses] == g
        except KeyError:
            table[responses] = g

        resp = score(g, secret)
        if resp == (4, 0):
            return

        S = tuple(s for s in S if score(s, g) == resp)

for secret in allcodes:
    solve(secret)

with open('table.txt', 'w') as fo:
    for responses in sorted(table):
        fo.write(responses + table[responses] + '\n')
