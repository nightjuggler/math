## primes.py

A script for analyzing [Goldbach partitions](https://en.wikipedia.org/wiki/Goldbach's_conjecture).

Currently testing the following observation/conjecture:

For every prime P, there exists a threshold N such that every even number > N is the sum of two primes > P.

N / P goes to 2 as P goes to infinity.

For example, the first few pairs (P, N) are (2, 4), (3, 8), (5, 16), (7, 20), (11, 28), ...

See, for example, `python primes.py maxevens 100000`

This suggests a sliding window approach to generating subsets of consecutive even numbers
from subsets of consecutive primes. (See, for example, `python primes.py sliding 10000`)

This resulted from the following observations:

<ol>
<li>For any two primes p1 and p2, both 1 mod 4, there exists at least one pair of primes q1 and q2, both 3 mod 4,
such that p1 + p2 = q1 + q2. (p1 can be equal to p2, and q1 can be equal to q2.)

Question: Is there always a pair q1 and q2 such that q1 is NOT equal to q2?

(See, for example, `python primes.py modstats 100000 4`)

<li>3 + (any prime that's 1 mod 6) can be written as the sum of two primes that are both 5 mod 6
<li>3 + (any prime that's 5 mod 6 and > 5) can be written as the sum of two primes that are both 1 mod 6

This means that every even number > 8 can be written as the sum of two primes > 3.

(See, for example, `python primes.py modstats 100000 6`)

</ol>
