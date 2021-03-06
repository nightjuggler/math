import itertools
import sys
import time

def init(max_number):
	global primes
	global is_prime

	print("Generating primes up to", max_number, "...")
	t1 = time.perf_counter()

	is_prime = [True] * (max_number + 1)
	is_prime[0] = False
	is_prime[1] = False

	for n in range(2, int(max_number ** 0.5) + 1):
		if is_prime[n]:
			m = n * n
			is_prime[m::n] = [False] * ((max_number - m) // n + 1)

	primes = list(itertools.compress(itertools.count(), is_prime))

	t2 = time.perf_counter()
	print("Time: {:.6f}s".format(t2 - t1))
	print("Number of primes:", len(primes))

def check_residue_filter(residue_filter):
	if not (isinstance(residue_filter, (list, tuple)) and len(residue_filter) % 2 == 0):
		print("The residue_filter parameter must be an even number of comma-separated integers!")
		return False
	for i in range(0, len(residue_filter), 2):
		residue = residue_filter[i]
		modulus = residue_filter[i+1]
		if not (isinstance(residue, int) and residue >= 0):
			print("Each residue of the residue_filter parameter must be an integer >= 0!")
			return False
		if not (isinstance(modulus, int) and modulus > 1):
			print("Each modulus of the residue_filter parameter must be an integer > 1!")
			return False
		if residue >= modulus:
			print("Each residue of the residue_filter parameter must be less than the modulus!")
			return
	return True

def filter_primes(residue_filter):
	global primes

	for i in range(0, len(residue_filter), 2):
		residue = residue_filter[i]
		modulus = residue_filter[i+1]

		print("Deleting primes congruent to {} mod {}".format(residue, modulus))

		new_primes = []
		for p in primes:
			if p % modulus == residue:
				is_prime[p] = False
			else:
				new_primes.append(p)

		num_before = len(primes)
		primes = new_primes
		num_after = len(primes)

		print("Deleted {} primes ({} - {})".format(num_before - num_after, num_before, num_after))

def gap_info(max_number, max_gaps=20):

	if not (isinstance(max_number, int) and max_number > 4):
		print("The max_number parameter must be an integer > 4!")
		return
	if not (isinstance(max_gaps, int) and max_gaps > 0):
		print("The max_gaps parameter must be an integer > 0!")
		return

	init(max_number)
	gap_count = [0] * max_gaps
	gaps = [0] * max_gaps
	max_gap = 0

	for p1, p2 in zip(primes[1:], primes[2:]):
		gap = ((p2 - p1) >> 1) - 1
		if gap < max_gaps:
			if gaps[gap] == 0:
				gaps[gap] = p1
			gap_count[gap] += 1
		elif gap > max_gap:
			max_gap = gap

	num_gaps = len(primes) - 2
	output_spec = " {:4} | {:8} {:>8} | {}"

	print("Number of gaps between primes from {} to {}: {}".format(primes[1], primes[-1], num_gaps))
	print("Number of gaps counted:", sum(gap_count))
	print("------+-------------------+------------------")
	print(" Size |       Count       | First Occurrence")
	print("------+-------------------+------------------")

	for gap, p, n in zip(itertools.count(), gaps, gap_count):
		gap = (gap + 1) << 1
		print(output_spec.format(gap, n, percent(n, num_gaps),
			"None" if p == 0 else "{} - {}".format(p, p + gap)))

	if max_gap:
		print("Found gaps up to size", (max_gap + 1) << 1)

def goldbach_partitions(N):
	if N < 4:
		return []
	if N == 4:
		return [(2, 2)]
	if N % 2 != 0:
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
	print(goldbach_partitions(N))

def goldbach_sliding_window(max_number=10000, start_prime_index=1, start_even=6, verbose=False):

	if not (isinstance(max_number, int) and max_number > 4):
		print("The max_number parameter must be an integer > 4!")
		return
	if not (isinstance(start_prime_index, int) and start_prime_index > 0):
		print("The start_prime_index parameter must be an integer > 0!")
		return
	if not (isinstance(start_even, int) and start_even % 2 == 0 and start_even > 4):
		print("The start_even parameter must be an even integer > 4!")
		return

	init(max_number)
	num_primes = len(primes)

	if start_prime_index + 10 >= num_primes:
		print("Not enough primes!")
		return

	qi = start_prime_index
	qj = qi + 10
	if qi > 10:
		n = primes[qi] * 2
		while primes[qj] < n:
			qj += 1
			if qj == num_primes:
				print("Not enough primes for a full window!")
				return
	even = start_even

	print("Generating consecutive evens starting with", even,
		"using primes from", primes[qi], "to", primes[num_primes - 1], "...")
	t1 = time.perf_counter()

	while True:
		q = primes[qi:qj]
		if verbose:
			print(qi, qj - qi, q[0], q[-1], even - 2)

		if q[0] * 2 > even:
			break

		sums = set()
		for i, p1 in enumerate(q[::-1], 1):
			for p2 in q[-i::-1]:
				if p1 + p2 < even:
					break
				sums.add(p1 + p2)
			if p1 == p2:
				break

		while even in sums:
			even += 2

		if qj == num_primes:
			break

		qi += 1
		n = primes[qi] * 2
		while primes[qj] < n:
			qj += 1
			if qj == num_primes:
				print("Last full window started with prime[{}] = {}".format(qi - 1, primes[qi - 1]),
					"and generated",
					"no evens!" if even == start_even else "evens up to " + str(even - 2))
				break

	t2 = time.perf_counter()
	print("Done!", "Generated",
		"no evens!" if even == start_even else "evens up to " + str(even - 2))
	print("Time: {:.6f}s".format(t2 - t1))

def goldbach_verify(max_number=10000, residue_filter=()):

	if not (isinstance(max_number, int) and max_number >= 4):
		print("The max_number parameter must be an integer >= 4!")
		return
	if not check_residue_filter(residue_filter):
		return

	if max_number % 2 != 0:
		max_number -= 1

	init(max_number)
	filter_primes(residue_filter)

	n = max_number
	half_n = n >> 1
	num_primes = len(primes)
	prime_index = num_primes >> 1

	if num_primes == 0:
		print("There are no primes!")
		return

	while prime_index + 1 < num_primes and primes[prime_index + 1] < half_n:
		prime_index += 1

	print("Checking for a Goldbach partition for every even number from", n, "down to 4 ...")
	t1 = time.perf_counter()

	while n > 2:
		while primes[prime_index] > half_n:
			if prime_index == 0:
				break
			prime_index -= 1
		i = prime_index
		while i >= 0:
			if is_prime[n - primes[i]]:
				break
			i -= 1
		else:
			print(n, "is not the sum of two primes!")
		n -= 2
		half_n -= 1

	t2 = time.perf_counter()
	print("Done!")
	print("Time: {:.6f}s".format(t2 - t1))

def goldbach_max_evens(max_number=10000, n_p_threshold=2.5, max_p_ratio=2.5, residue_filter=()):

	if not (isinstance(max_number, int) and max_number >= 4):
		print("The max_number parameter must be an integer >= 4!")
		return
	if not (isinstance(n_p_threshold, (float, int)) and n_p_threshold >= 2):
		print("The n_p_threshold parameter must be a number >= 2!")
		return
	if not (isinstance(max_p_ratio, (float, int)) and max_p_ratio >= 1):
		print("The max_p_ratio parameter must be a number >= 1!")
		return
	if not check_residue_filter(residue_filter):
		return

	if max_number % 2 != 0:
		max_number -= 1

	init(max_number)
	filter_primes(residue_filter)

	n = max_number
	half_n = n >> 1
	num_primes = len(primes)
	prime_index = num_primes >> 1

	if num_primes == 0:
		print("There are no primes!")
		return

	while prime_index > 0 and primes[prime_index] > half_n:
		prime_index -= 1
	while prime_index + 1 < num_primes and primes[prime_index + 1] < half_n:
		prime_index += 1

	print("Computing max evens for {} primes (up to {}) ...".format(prime_index + 1, primes[prime_index]))
	t1 = time.perf_counter()

	max_evens = [0] * (prime_index + 1)

	while n > 2:
		while primes[prime_index] > half_n:
			if prime_index == 0:
				break
			prime_index -= 1
		i = prime_index
		while i >= 0:
			if is_prime[n - primes[i]]:
				if max_evens[i] == 0:
					max_evens[i] = n
				break
			i -= 1
		else:
			print(n, "is not the sum of two primes!")
		n -= 2
		half_n -= 1

	t2 = time.perf_counter()
	print("Time: {:.6f}s".format(t2 - t1))
	print("Averaging N/P ...")

	sum_n_p = 0.0
	num_n_p = 0
	previous_n = 0
	num_less_than_previous_n = 0
	max_p = int(max_number / max_p_ratio)

	for p, n in zip(primes, max_evens):
		if p > max_p:
			break

		if n < previous_n:
			n = previous_n
			num_less_than_previous_n += 1

		n_p = float(n) / p
		if n_p >= n_p_threshold or n_p < 2.0:
			print(p, n, n_p)

		sum_n_p += n_p
		num_n_p += 1
		previous_n = n

	if num_n_p == 0:
		print("Nothing to average!", "(prime[0] = {} >= {}/4)".format(primes[0], max_number))
		return

	i = num_n_p - 1
	print("Stopped at prime[{}] = {} (N = {}, N/P = {})".format(i, primes[i], max_evens[i], n_p))
	print("Average N/P:", sum_n_p / num_n_p)
	print("Number of N less than previous N:", num_less_than_previous_n)

def percent(a, b):
	return "({:.2f}%)".format(100.0 * a / b)

def print_mod_count(count):
	mod = "mod {}:".format(len(count))
	num_primes = len(primes)
	for i, n in enumerate(count):
		if n > 0:
			print(i, mod, n, percent(n, num_primes))

def compute_mod_stats1(num_evens, mod):
	evens = [0] * num_evens
	mod_is_even = mod % 2 == 0

	count = [0] * mod
	prime_mods = [p % mod for p in primes]
	for m in prime_mods:
		count[m] += 1

	print_mod_count(count)

	from itertools import count as icount

	for i, p1, m1 in zip(icount(), primes, prime_mods):
		if i & 127 == 0:
			print("\rComputing sums p1 + p2 where p1 =", p1, "and p2 >= p1 ...", end="")
			sys.stdout.flush()
		for j, p2, m2 in zip(icount(), primes[i:], prime_mods[i:]):
			k = ((p1 + p2) >> 1) - 3
			if k >= num_evens:
				if j == 0:
					print("\nDone @ prime[{}] = {}".format(i, p1))
					return evens
				break

			# When mod is 4, m1 + m2 can be 2 (1+1), 4 (1+3 or 3+1), or 6 (3+3)
			if mod_is_even:
				evens[k] |= 1 << (((m1 + m2) >> 1) - 1)
			else:
				evens[k] |= 1 << (m1 + m2)
	return evens

def compute_mod_stats2(num_evens, mod):
	evens = [0] * num_evens
	mod_is_even = mod % 2 == 0

	count = [0] * mod
	for p in primes:
		count[p % mod] += 1

	print_mod_count(count)

	for i, p1 in enumerate(primes):
		m1 = p1 % mod
		if i & 127 == 0:
			print("\rComputing sums p1 + p2 where p1 =", p1, "and p2 >= p1 ...", end="")
			sys.stdout.flush()
		for p2 in primes[i:]:
			k = ((p1 + p2) >> 1) - 3
			if k >= num_evens:
				if p2 == p1:
					print("\nDone @ prime[{}] = {}".format(i, p1))
					return evens
				break

			# When mod is 4, m1 + m2 can be 2 (1+1), 4 (1+3 or 3+1), or 6 (3+3)
			m2 = p2 % mod
			if mod_is_even:
				evens[k] |= 1 << (((m1 + m2) >> 1) - 1)
			else:
				evens[k] |= 1 << (m1 + m2)
	return evens

def compute_mod_stats3(num_evens, mod):
	evens = [0] * num_evens
	mod_is_even = mod % 2 == 0

	count = [0] * mod
	for p in primes:
		count[p % mod] += 1

	print_mod_count(count)

	for i, p1 in enumerate(primes):
		m1 = p1 % mod
		if i & 127 == 0:
			print("\rComputing sums p1 + p2 where p1 =", p1, "and p2 >= p1 ...", end="")
			sys.stdout.flush()
		for p2 in primes[i:]:
			k = ((p1 + p2) >> 1) - 3
			if k >= num_evens:
				if p2 == p1:
					print("\nDone @ prime[{}] = {}".format(i, p1))
					return evens
				break

			m2 = p2 % mod
			if mod_is_even:
				# If the modulus is even, m1 and m2 must both be odd.
				# So shifting right is equivalent to subtracting 1 and dividing by 2.
				evens[k] |= 1 << ((m1 >> 1) * (mod >> 1) + (m2 >> 1))
			else:
				evens[k] |= 1 << (m1 * mod + m2)
	return evens

def gen_decode_bits_v1(mod):
	if mod % 2 == 0:
		shift = mod - 1
		initial_values = (2, 2)
	else:
		shift = 2 * mod - 1
		initial_values = (0, 1)

	max_parts = 2
	width = len(str((mod - 1) << 1))
	part_spec = "{{:>{}}}".format(width)
	join_spec = "{{:>{}}}:".format(max_parts * (width + 1) - 1)

	def decode_bits(x):
		sums = []
		m1_plus_m2, step = initial_values
		for i in range(shift):
			if x & (1 << i) != 0:
				sums.append(part_spec.format(m1_plus_m2))
			m1_plus_m2 += step
		return join_spec.format(",".join(sums))

	return shift, decode_bits

def gen_decode_bits_v3(mod):
	if mod % 2 == 0:
		shift = (mod >> 1) ** 2
		initial_values = (1, 1, 2)
		max_parts = mod >> 1
	else:
		shift = mod ** 2
		initial_values = (0, 0, 1)
		max_parts = mod

	width = len(str(mod - 1))
	part_spec = "{{:>{}}}+{{:>{}}}".format(width, width)
	join_spec = "{{:>{}}}:".format(2 * max_parts * (width + 1) - 1)

	def decode_bits(x):
		sums = []
		m1, m2, step = initial_values
		for i in range(shift):
			if x & (1 << i) != 0:
				sums.append(part_spec.format(m1, m2))
			m2 += step
			if m2 >= mod:
				m2 -= mod
				m1 += step
		return join_spec.format(",".join(sums))

	return shift, decode_bits

def goldbach_mod_stats(num_evens=10000, mod=4, start_prime_index=1, version=3,
	delete_prime_indices=(), residue_filter=()):

	if not (isinstance(num_evens, int) and num_evens > 0):
		print("The num_evens parameter must be an integer > 0!")
		return
	if not (isinstance(mod, int) and mod > 2):
		print("The mod parameter must be an integer > 2!")
		return
	if not (isinstance(start_prime_index, int) and start_prime_index > 0):
		print("The start_prime_index parameter must be an integer > 0!")
		return
	if not isinstance(delete_prime_indices, (list, tuple)):
		print("The delete_prime_indices parameter must be a list or tuple!")
		return
	for i in delete_prime_indices:
		if not (isinstance(i, int) and i >= 0):
			print("The delete_prime_indices parameter must be a list or tuple of integers >= 0!")
			return

	if version == 3:
		compute_mod_stats = compute_mod_stats3
		shift, decode_bits = gen_decode_bits_v3(mod)
	elif version == 2:
		compute_mod_stats = compute_mod_stats2
		shift, decode_bits = gen_decode_bits_v1(mod)
	elif version == 1:
		compute_mod_stats = compute_mod_stats1
		shift, decode_bits = gen_decode_bits_v1(mod)
	else:
		print("The version parameter must be 1, 2, or 3!")
		return

	if shift >= 32:
		print("The mod parameter is too big!")
		return
	if not check_residue_filter(residue_filter):
		return

	init(2 * (num_evens + 2)) # Add 2 since we're skipping the first two evens (2 and 4)

	if start_prime_index == 1:
		print("Deleting", primes[0])
	else:
		print("Deleting the first", start_prime_index, "primes:", primes[:start_prime_index])
	del primes[:start_prime_index]

	for diff, i in enumerate(delete_prime_indices, start=start_prime_index):
		# For example 6,12,14,17,19,22 corresponds to the primes 17,41,47,61,71,83
		if i >= start_prime_index:
			p = primes[i - diff]
			print("Deleting", p, "({} mod 4)".format(p % 4), "({} mod 6)".format(p % 6))
			del primes[i - diff]

	filter_primes(residue_filter)

	t1 = time.perf_counter()
	evens = compute_mod_stats(num_evens, mod)
	t2 = time.perf_counter()
	print("Time: {:.6f}s".format(t2 - t1))

	cases = {}

	def cases_str(bits, n):
		s = [str(x) for x in cases[bits]]
		if n > 5:
			s.insert(-1, "...")
		return "[{}]".format(", ".join(s))

	def cases_add(bits, even):
		even = (even + 3) << 1
		s = cases.get(bits)
		if s is None:
			cases[bits] = [even]
		elif len(s) < 5:
			s.append(even)
		else:
			s[-1] = even

	if shift > 16:
		count = {}
		for even, bits in enumerate(evens):
			count[bits] = count.get(bits, 0) + 1
			cases_add(bits, even)

		for bits, n in sorted(count.iteritems()):
			print(decode_bits(bits), n, percent(n, num_evens), cases_str(bits, n))
	else:
		count = [0] * (1 << shift)
		for even, bits in enumerate(evens):
			count[bits] += 1
			cases_add(bits, even)

		for bits, n in enumerate(count):
			if n > 0:
				print(decode_bits(bits), n, percent(n, num_evens), cases_str(bits, n))

def residue_distribution(max_number=10000, mod=4, residue_filter=()):

	if not (isinstance(max_number, int) and max_number >= 4):
		print("The max_number parameter must be an integer >= 4!")
		return
	if not (isinstance(mod, int) and mod > 2):
		print("The mod parameter must be an integer > 2!")
		return
	if not check_residue_filter(residue_filter):
		return

	init(max_number)
	filter_primes(residue_filter)

	count = [0] * mod
	for p in primes:
		count[p % mod] += 1

	print_mod_count(count)

if __name__ == "__main__":
	import main
	main.run_command(sys.argv[1:], "partitions", {
		"gaps": (gap_info, [10000, 20]),
		"maxevens": (goldbach_max_evens, [10000, 2.5, 2.5, ()]),
		"modcount": (residue_distribution, [10000, 4, ()]),
		"modstats": (goldbach_mod_stats, [10000, 4, 1, 3, (), ()]),
		"partitions": (print_goldbach_partitions, [14]),
		"sliding": (goldbach_sliding_window, [10000, 1, 6, False]),
		"verify": (goldbach_verify, [10000, ()]),
	})
