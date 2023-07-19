class MyDecimal(object):
	def __init__(self, value=0, precision=0):
		#
		# The precision arg is ignored if the value is a string
		#
		if isinstance(value, str):
			value, *b = value.split('.')
			if b:
				b, = b
				b = b.rstrip('0')
			else:
				b = ''
			value = int(value.replace(',', ''))
			if precision := len(b):
				value *= 10**precision
				if value < 0:
					value -= int(b)
				else:
					value += int(b)
		else:
			if not isinstance(value, int):
				raise TypeError('MyDecimal must be initialized from an int or str')
			if not isinstance(precision, int):
				raise TypeError('MyDecimal precision must be an int')
		while not (value % 10):
			value //= 10
			precision -= 1
		self.value = value, precision

	@classmethod
	def get_other(cls, other):
		if isinstance(other, cls):
			return other.value
		if isinstance(other, int):
			return other, 0
		raise TypeError('Right operand must be MyDecimal or int')

	def get_normalized(self, other):
		v1, p1 = self.value
		v2, p2 = self.get_other(other)
		if p1 < p2:
			return v1 * 10**(p2-p1), v2, p2
		return v1, v2 * 10**(p1-p2), p1

	def round(self, precision=2, *, down=False):
		v, p = self.value
		if p < precision:
			self.value = v * 10**(precision-p), precision
		elif p > precision:
			if negative := v < 0: v = -v
			v, remainder = divmod(v, 10**(p-precision))
			if not down and remainder // 10**(p-precision-1) >= 5: v += 1
			if negative: v = -v
			self.value = v, precision
		return self

	def __add__(self, other):
		self, other, precision = self.get_normalized(other)
		return MyDecimal(self + other, precision)

	def __sub__(self, other):
		self, other, precision = self.get_normalized(other)
		return MyDecimal(self - other, precision)

	def __mul__(self, other):
		v1, p1 = self.value
		v2, p2 = self.get_other(other)
		return MyDecimal(v1 * v2, p1 + p2)

	def __str__(self):
		value, precision = self.value
		if not precision:
			return format(value, ',')
		if precision < 0:
			return format(value * 10**-precision, ',')
		if value < 0:
			a, b = divmod(-value, 10**precision)
			a = -a
		else:
			a, b = divmod(value, 10**precision)
		return f'{a:,}.{b:0{precision}}'

	def __repr__(self):
		return self.__str__()

	def __hash__(self):
		return hash(self.value)

	def __lt__(self, other):
		self, other, precision = self.get_normalized(other)
		return self < other

	def __le__(self, other):
		self, other, precision = self.get_normalized(other)
		return self <= other

	def __eq__(self, other):
		self, other, precision = self.get_normalized(other)
		return self == other

	def __ne__(self, other):
		self, other, precision = self.get_normalized(other)
		return self != other

	def __gt__(self, other):
		self, other, precision = self.get_normalized(other)
		return self > other

	def __ge__(self, other):
		self, other, precision = self.get_normalized(other)
		return self >= other
