import sys

def init(max_number):
	global primes
	global is_prime

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

def is_sum_of_two_primes(N):
	# 1. From Goldbach's conjecture, we know every even number (> 2) is the sum of two primes.
	# 2. An odd number N is the sum of two primes if and only if N-2 is prime.
	return N > 2 and (N % 2 == 0 or is_prime[N - 2])

def goldbach_partitions(N):
	if N < 4:
		return []
	if N == 4:
		return [(2, 2)]
	if N % 2 == 1:
		return [(2, N - 2)] if is_prime[N - 2] else []

	partitions = []

	for p in primes:
		n = N - p
		if n < p:
			break
		if is_prime[n]:
			partitions.append((p, n))

	return partitions

def print_goldbach_partitions(N=14):
	init(N)
	print goldbach_partitions(N)

def goldbach_sliding_window(max_number=10000):
	if not (isinstance(max_number, int) and max_number > 40):
		print "The max_number parameter must be an integer > 40!"
		return

	init(max_number)
	del primes[0]
	num_primes = len(primes)

	even = 4
	qi = 0
	qj = 10

	while True:
		q = primes[qi:qj]

		print qi, qj-qi, q[0], q[-1], even

		if q[0] * 2 > even + 2:
			break

		j = len(q) - 1
		while j != 0 and q[j] << 1 > even:
			j -= 1

		sums = []
		for i, p1 in enumerate(q):
			for p2 in q[i if i > j else j:]:
				n = p1 + p2
				if n > even:
					sums.append(n)

		for m in sorted(sums):
			if m == even + 2:
				even = m
			elif m != even:
				break

		if qj == num_primes:
			break

		qi += 1
		n = primes[qi] * 2

		while primes[qj] < n:
			qj += 1
			if qj == num_primes:
				break

		if qj - qi < 10:
			qj = qi + 10
			if qj > num_primes:
				break

	print "Done!", even

def goldbach_max_evens(max_number=10000):
	if not (isinstance(max_number, int) and max_number > 4):
		print "The max_number parameter must be an integer > 4!"
		return

	if max_number % 2 == 1:
		max_number -= 1

	init(max_number)

	prime_index = len(primes) >> 1
	half_max = max_number >> 1

	while primes[prime_index] > half_max:
		prime_index -= 1
	while primes[prime_index + 1] < half_max:
		prime_index += 1

	print "Computing max evens for {} primes (up to {}) ...".format(prime_index + 1, primes[prime_index])
	max_evens = [0] * (prime_index + 1)

	n = max_number
	while n > 2:
		half_n = n >> 1
		while primes[prime_index] > half_n:
			prime_index -= 1
		i = prime_index
		while i >= 0:
			if is_prime[n - primes[i]]:
				if max_evens[i] == 0:
					max_evens[i] = n
				break
			i -= 1
		n -= 2

	print "Averaging N/P ..."

	sum_n_p = 0.0
	num_n_p = 0

	previous_n = 0
	num_less_than_previous_n = 0

	for p, n in zip(primes, max_evens):
		if p * 4 >= max_number:
			break

		if n < previous_n:
			n = previous_n
			num_less_than_previous_n += 1

		n_p = float(n) / p
		if n_p > 2.5:
			print p, n, n_p

		sum_n_p += n_p
		num_n_p += 1

		previous_n = n

	if num_n_p == 0:
		print "Nothing to average!", "(prime[0] = {} >= {}/4)".format(primes[0], max_number)
		return

	i = num_n_p - 1
	print "Stopped at prime[{}] = {} (N = {}, N/P = {})".format(num_n_p, primes[i], max_evens[i], n_p)
	print "Average N/P:", sum_n_p / num_n_p
	print "Number of N less than previous N:", num_less_than_previous_n

def goldbach_mod_stats(num_evens=10000, mod=4, start_prime_index=1):
	if not (isinstance(num_evens, int) and num_evens > 0):
		print "The num_evens parameter must be an integer > 0!"
		return
	if not (isinstance(mod, int) and mod > 2):
		print "The mod parameter must be an integer > 2!"
		return
	if not (isinstance(start_prime_index, int) and start_prime_index > 0):
		print "The start_prime_index parameter must be an integer > 0!"
		return

	init(2 * (num_evens + 2)) # Add 2 since we're skipping the first two evens (2 and 4)
	evens = [0] * num_evens

	if start_prime_index == 1:
		print "Deleting", primes[0]
		del primes[0]
#		for d, i in enumerate([5, 11, 13, 16, 18, 21]):
#			p = primes[i - d]
#			print "Deleting", p, "({} mod 4)".format(p % 4), "({} mod 6)".format(p % 6)
#			del primes[i - d]
	else:
		print "Deleting the first", start_prime_index, "primes:", primes[:start_prime_index]
		del primes[:start_prime_index]

	mod_is_even = mod % 2 == 0
	prime_mods = [p % mod for p in primes]
	count = [0] * mod

	for m in prime_mods:
		count[m] += 1

	num_primes = float(len(primes))
	for i, n in enumerate(count):
		if n > 0:
			print "{} mod {}: {} ({:.2f}%)".format(i, mod, n, 100 * n / num_primes)

	done = False
	for i, (p1, m1) in enumerate(zip(primes, prime_mods)):
		if i & 127 == 0:
			print "\rComputing sums p1 + p2 where p1 =", p1, "and p2 >= p1 ...",
			sys.stdout.flush()
		for j, (p2, m2) in enumerate(zip(primes[i:], prime_mods[i:])):
			k = ((p1 + p2) >> 1) - 3
			if k >= num_evens:
				if j == 0:
					done = True
				break

			# When mod is 4, m1 + m2 can be 2 (1+1), 4 (1+3 or 3+1), or 6 (3+3)
			if mod_is_even:
				evens[k] |= 1 << (((m1 + m2) >> 1) - 1)
			else:
				evens[k] |= 1 << (m1 + m2)
		if done:
			print "\nDone @ prime[{}] = {}".format(i, primes[i])
			break

	shift = mod - 1 if mod_is_even else 2 * mod - 1
	count = [0] * (1 << shift)
	cases = [[] for i in xrange(1 << shift)]
	for i, n in enumerate(evens):
		count[n] += 1
		s = cases[n]
		if len(s) < 5:
			s.append((i + 3) << 1)
		else:
			s[-1] = (i + 3) << 1

	num_evens = float(num_evens)
	prefix_spec = "{{:0{}b}}:".format(shift)
	percent_spec = "({:.2f}%)"
	for i, (n, s) in enumerate(zip(count, cases)):
		if n > 0:
			s = [str(x) for x in s]
			if n > 5:
				s.insert(-1, "...")
			s = "[{}]".format(", ".join(s))
			print prefix_spec.format(i), n, percent_spec.format(100 * n / num_evens), s

def main(args):
	commands = {
		"maxevens": (goldbach_max_evens, [10000]),
		"modstats": (goldbach_mod_stats, [10000, 4, 1]),
		"partitions": (print_goldbach_partitions, [14]),
		"sliding": (goldbach_sliding_window, [10000]),
	}
	command = args.pop(0)

	if command not in commands:
		print "Please enter a valid command!"
		return

	function, params = commands[command]

	if len(args) > len(params):
		print "Too many parameters after the command!"
		return

	for i, (arg, param) in enumerate(zip(args, params)):
		try:
			params[i] = int(arg)
		except ValueError:
			i += 1
			print "The {}{} parameter after the command must be an integer!".format(i,
				["th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th"][i % 10])
			return

	function(*params)

if __name__ == "__main__":
	main(sys.argv[1:])
