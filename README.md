# Solving Mastermind

Responses:

    +   correct color in correct place
    -   only color correct

Here are some example of how to invoke the program:

1.) Program guesses it's own randomly generated code:

    $ python mastermind.py -
    secret: BGRB
    1 BBGG +--
    2 BGBK ++-
    3 BBRW ++-
    4 BGRB ++++

2.) With no arguments, you can enter your own responses.

    $ python mastermind.py
    BBGG: <enter combination of '+' and '-'>


# How is works

Donald Knuth developed a mastermind code breaking algorithm in 1977, and he
demonstrated that only 5 guesses are needed to break the code [here](https://www.cs.uni.edu/~wallingf/teaching/cs3530/resources/knuth-mastermind.pdf).
A description of the algorithm can be found on [Wikipedia](https://en.wikipedia.org/wiki/Mastermind_(board_game)#Worst_case:_Five-guess_algorithm), as well as on many other places.

Although I was able to create a working program quickly, I found the various
descriptions of the algorithm very confusing, and it took me a while to get
to the bottom of how it works.   So what follows is my own description.

The algorithm that progressively reduces the number of possible codes.
It starts by taking creating a list of all 1296 (6^4) possible codes `S`,
and an initial guess of `BBGG`.
Obviously, a response of `(4, 0)` terminates the algorithm.
After each response `resp`, we only keep the codes `S` which would give the
same response to the guess `g`:

    S = [s for s in S if score(s, g) == resp]

That is, the possible codes must give the same response to the guess.

As a first step (towards a better algorithm), we could simply randomly choose
any element in `S` as the next guess.  I have tried this, and it works
surprisingly well (with an average of about 4.65 guesses) but in some cases
more then 5 guesses are necessary to break the code.

Instead, we pick a guess (from *all* codes) which minimizes the
maximum number of remaining `S` over all 14 possible guesses:

    min(allcodes, key=lambda p: max(sum(score(s, p) == resp for s in S)
                                        for resp in responses))

This guess `g` will result in the minimum elements `S` remaining, in the
next step, *regardless* of what the response actually is.
As we pick the guess from all codes (not just the possible codes `S`),
we may (and often do) pick a guess which is an impossible solution.
However, we do this in order to minimize the worst response such that `S` is
smallest for the next iteration.

This can be regarded as an example of the Minimax decision rule, as we
minimize the maximum (worst possible case depending on the (yet unknown)
response).

This algorithm has an average of 4.76 guesses, but never more then 5 guesses.
