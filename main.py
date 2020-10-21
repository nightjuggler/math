def ordinal(n):
	return str(n) + ("th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th")[n % 10]

def param_must_be(i, description):
	print("The {} parameter after the command must be {}!".format(ordinal(i + 1), description))

def parse_number(arg, convert=int):
	try:
		return convert(arg)
	except ValueError:
		return None

def parse_list(arg):
	param = []

	arg = arg.strip(",")
	if arg == "":
		return param

	for arg in arg.split(","):
		arg = parse_number(arg)
		if arg is None:
			return None
		param.append(arg)

	return param

def run_command(args, default_command, commands):
	command = args.pop(0) if args else default_command

	if command not in commands:
		print("Please enter a valid command!")
		return

	function, params = commands[command]

	if len(args) > len(params):
		print("Too many parameters after the command!")
		return

	for i, (arg, param) in enumerate(zip(args, params)):

		if isinstance(param, bool):
			if arg in ("1", "on", "true", "yes"):
				param = True
			elif arg in ("0", "off", "false", "no"):
				param = False
			else:
				param_must_be(i, "a boolean")
				return
		elif isinstance(param, int):
			param = parse_number(arg)
			if param is None:
				param_must_be(i, "an integer")
				return
		elif isinstance(param, float):
			param = parse_number(arg, float)
			if param is None:
				param_must_be(i, "a number")
				return
		elif isinstance(param, (list, tuple)):
			param = parse_list(arg)
			if param is None:
				param_must_be(i, "a comma-separated list of integers")
				return
		else:
			print("Unable to parse the", ordinal(i+1), "parameter after the command!")
			return

		params[i] = param

	function(*params)
