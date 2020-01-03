## primes.py

A script for analyzing [Goldbach partitions](https://en.wikipedia.org/wiki/Goldbach's_conjecture).

Currently testing the following observation/conjecture and its implications:

For every prime P, there exists a threshold N such that every even number > N is the sum of two primes > P.

N is the lowest such threshold, i.e. N itself is not the sum of two primes > P.

N / P goes to 2 as P goes to infinity.

For example, the first few pairs (P, N) are (2, 4), (3, 8), (5, 16), (7, 20), (11, 28), ...

(See, for example, `python primes.py maxevens 100000`)

This suggests a sliding window approach to generating all even numbers > 2 as sums of two primes
by generating subsets of consecutive even numbers from subsets of consecutive primes.
(See, for example, `python primes.py sliding 50000` which runs such an algorithm to generate
all even numbers from 4 to 99,650.)

This resulted from observing correlations between sums of two primes of certain residue classes.

For example:

<ol>
<li>For any two primes P1 and P2, both 1 mod 4, there exists at least one pair of primes Q1 and Q2, both 3 mod 4,
such that P1 + P2 = Q1 + Q2. (P1 can be equal to P2, and Q1 may be equal to Q2.)

(See, for example, `python primes.py modstats 100000 4`)

<li>3 + (any prime that's 1 mod 6) is the sum of two primes that are both 5 mod 6, and

3 + (any prime that's 5 mod 6 and > 5) is the sum of two primes that are both 1 mod 6.

This means that every even number > 8 is the sum of two primes > 3.

(See, for example, `python primes.py modstats 100000 6`)

</ol>
