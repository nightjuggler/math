def ordinal(n):
	return str(n) + ("th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th")[n % 10]

def parse_number(arg, convert=int):
	try:
		return convert(arg)
	except ValueError:
		return None

def run_command(args, default_command, commands):
	command = args.pop(0) if args else default_command

	if command not in commands:
		print "Please enter a valid command!"
		return

	function, params = commands[command]

	if len(args) > len(params):
		print "Too many parameters after the command!"
		return

	for i, (arg, param) in enumerate(zip(args, params)):

		if isinstance(param, int):
			param = parse_number(arg)
			if param is None:
				print "The", ordinal(i+1), "parameter after the command must be an integer!"
				return
		elif isinstance(param, float):
			param = parse_number(arg, float)
			if param is None:
				print "The", ordinal(i+1), "parameter after the command must be a number!"
				return
		elif isinstance(param, (list, tuple)):
			param = []
			for arg in arg.split(","):
				arg = parse_number(arg)
				if arg is None:
					print "The", ordinal(i+1), ("parameter after the command must be "
						"a comma-separated list of integers!")
					return
				param.append(arg)
		else:
			print "Unable to parse the", ordinal(i+1), "parameter after the command!"
			return

		params[i] = param

	function(*params)
