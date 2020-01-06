import itertools
import os.path
import sys
import time

def square_partitions(N):
	partitions = []
	for a in xrange(int(N ** 0.5) + 1):
		a2 = a**2
		b = int((N - a2) ** 0.5)
		if a > b:
			break
		if a2 + b**2 == N:
			partitions.append((a, b))

	print partitions

def evens_from_odds(max_even, first_odd=3, csv=0):

	if not isinstance(max_even, int):
		print "The max_even parameter must be an integer!"
		return
	if not (isinstance(first_odd, int) and first_odd % 2 != 0):
		print "The first_odd parameter must be an odd integer!"
		return
	if not (isinstance(csv, int) and 0 <= csv <= 2):
		print "The csv parameter must be an integer between 0 and 2!"
		return

	if csv == 1:
		print "numOdds,maxEven"
		csv_format = lambda n, e: str(n) + "," + str(e)
	elif csv == 2:
		print "var evensFromOddsData = ["
		csv_format = lambda n, e: "{numOdds:" + str(n) + ",maxEven:" + str(e) + "},"

	odds = [first_odd]
	first_even = first_odd * 2
	next_even = first_even + 2

	while next_even <= max_even:

		x = odds[-1] + 2
		odds.append(x)

		best_x = 0
		best_x_even = 0

		while True:
			j = len(odds) - 1
			while j != 0 and odds[j] * 2 >= next_even:
				j -= 1

			sums = {n1 + n2
				for i, n1 in enumerate(odds)
					for n2 in odds[i if i > j else j:] if n1 + n2 >= next_even}

			x_even = next_even
			while x_even in sums:
				x_even += 2

			if x_even > next_even and x_even >= best_x_even:
				best_x = x
				best_x_even = x_even

			x += 2
			if x + first_odd > next_even:
				break
			odds[-1] = x

		odds[-1] = best_x
		next_even = best_x_even
		if csv:
			print csv_format(len(odds), next_even - 2)

	if csv:
		if csv == 2:
			print "];"
		return

	oddsstr = "{" + ", ".join(map(str, odds)) + "}"
	percent = "{:.2f}%".format(100.0 * len(odds) / ((next_even - 1 - first_odd) / 2))

	print "Consecutive evens from", first_even, "to", next_even - 2,
	print "can be expressed as sums of two odds from the set", oddsstr,
	print "which has", len(odds), "elements =", percent, "of the odd numbers",
	print "from", first_odd, "to", next_even - 3

def consecutive_evens(numbers, start=6):

	if not isinstance(numbers, (list, tuple)):
		print "The numbers parameter must be a list of integers!"
		return
	for n in numbers:
		if not isinstance(n, int):
			print "The numbers parameter must be a list of integers!"
			return
	if not (isinstance(start, int) and start % 2 == 0):
		print "The start parameter must be an even integer!"
		return

	sums = {n1 + n2 for i, n1 in enumerate(numbers) for n2 in numbers[i:]}

	even = start
	while even in sums:
		even += 2

	if even == start:
		print "Generated no consecutive evens starting at", start
	else:
		print "Generated {} consecutive evens from {} to {} using {} numbers".format(
			(even - start)/2, start, even - 2, len(numbers))

def naive_sieve(max_number):
	global primes
	global is_prime

	print "Generating primes up to", max_number, "..."
	t1 = time.clock()

	primes = []
	is_prime_len = max_number + 1
	is_prime = [True] * is_prime_len
	is_prime[0] = False
	is_prime[1] = False

	for n in xrange(2, is_prime_len):
		if is_prime[n]:
			primes.append(n)
			for m in xrange(n + n, is_prime_len, n):
				is_prime[m] = False

	t2 = time.clock()
	print "Time: {:.6f}s".format(t2 - t1)
	print "Number of primes:", len(primes)

def sieve(max_number):
	global primes
	global is_prime

	print "Generating primes up to", max_number, "..."
	t1 = time.clock()

	is_prime = [True] * (max_number + 1)
	is_prime[0] = False
	is_prime[1] = False

	for n in xrange(2, int(max_number ** 0.5) + 1):
		if is_prime[n]:
			m = n * n
			is_prime[m::n] = [False] * len(is_prime[m::n])

	primes = list(itertools.compress(itertools.count(), is_prime))

	t2 = time.clock()
	print "Time: {:.6f}s".format(t2 - t1)
	print "Number of primes:", len(primes)

def read_primes(N=1):
	if not (isinstance(N, int) and 1 <= N <= 50):
		print "The N parameter must be an integer between 1 and 50!"
		return

	filename = "data/primes" + str(N) + ".txt"
	if not os.path.exists(filename):
		print "The file", filename, "does not exist!"
		return

	print "Reading", filename, "..."
	primes = []
	with open(filename) as f:
		line = f.next().strip()
		if not line.endswith("(from primes.utm.edu)"):
			print "Unexpected format for line 1!"
			return
		line = f.next().strip()
		if line != "":
			print "Unexpected format for line 2!"
			return
		line_number = 2
		for line in f:
			line_number += 1
			line = line.strip().split()
			if len(line) != 8:
				print "Expected 8 columns on line {}!".format(line_number)
				return
			try:
				line = map(int, line)
			except ValueError:
				print "One of the columns on line {} is not an integer!".format(line_number)
				return
			primes.extend(line)

	print "Read {:,} primes!".format(len(primes))
	return primes

if __name__ == "__main__":
	import main
	main.run_command(sys.argv[1:], "square_partitions", {
		"consecutive_evens": (consecutive_evens, [[3, 5, 9, 13, 15, 29, 33, 35, 47, 51], 6]),
		"evens_from_odds": (evens_from_odds, [100, 3, 0]),
		"naive_sieve": (naive_sieve, [10000]),
		"read_primes": (read_primes, [1]),
		"sieve": (sieve, [10000]),
		"square_partitions": (square_partitions, [2020]),
	})
