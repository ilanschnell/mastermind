# Solving Mastermind

Here are some example of how to invoke the program.

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

The Donald Knuth developed the code breaking algorithm in 1977, which
can be found [here](https://www.cs.uni.edu/~wallingf/teaching/cs3530/resources/knuth-mastermind.pdf).
A description of the algorithm can be found on [Wikipedia](https://en.wikipedia.org/wiki/Mastermind_(board_game)), as well as on many other places.
