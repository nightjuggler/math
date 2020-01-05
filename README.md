## primes.py

A script for analyzing [Goldbach partitions](https://en.wikipedia.org/wiki/Goldbach's_conjecture).

Currently testing the following observation/conjecture (12/31/2019) and its implications:

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

Further observations (verified for all evens up to 50 million):

* Every even number > 68 is the sum of two primes neither of which is 1 mod 10.
  (`python primes.py verify 50000000 1,10`) (1/3/2020)
* Every even number > 68 is the sum of two primes neither of which is 7 mod 10.
  (`python primes.py verify 50000000 7,10`) (1/3/2020)
* Every even number > 152 is the sum of two primes neither of which is 3 mod 10.
  (`python primes.py verify 50000000 3,10`) (1/3/2020)
* Every even number > 152 is the sum of two primes neither of which is 9 mod 10.
  (`python primes.py verify 50000000 9,10`) (1/3/2020)

* Every even number > 2 is the sum of two primes neither of which is 1 mod 8.
  (`python primes.py verify 50000000 1,8`) (1/4/2020)
  This implies that one can express every even number > 2 as the sum of two primes
  using only 3/4 of all primes.
* Every even number > 56 is the sum of two primes neither of which is 3 mod 8.
  (`python primes.py verify 50000000 3,8`) (1/4/2020)
* Every even number > 188 is the sum of two primes neither of which is 5 mod 8.
  (`python primes.py verify 50000000 5,8`) (1/4/2020)
* Every even number > 188 is the sum of two primes neither of which is 7 mod 8.
  (`python primes.py verify 50000000 7,8`) (1/4/2020)

* Every even number > 2 is the sum of two primes neither of which is 1 mod 7 or 4 mod 7.
  (`python primes.py verify 50000000 4,7,1,7`) (1/4/2020)
  This implies that one can express every even number > 2 as the sum of two primes
  using only 2/3 of all primes.

* Every even number > 2 is the sum of two primes neither of which is 1, 4, 6, 8, 9, 10, or 15 mod 17.
  (`python primes.py verify 50000000 1,17,4,17,6,17,8,17,9,17,10,17,15,17`) (1/4/2020)
  This omits (3001134 - 1688268) / 3001134 = 43.75% of primes.
