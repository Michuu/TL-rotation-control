
get_ = {
	'info' : b'in',
	'status' : b'gs',
	'position': b'gp',
	'stepsize' : b'gj'
	}

set_ = {
	'stepsize' : b'sj'
	}

mov_ = {
	'home' : b'ho',
	'forward' : b'fw',
	'backward' : b'bw',
	'absolute' : b'ma',
	'relative' : b'mr'
	}


def commands():
	return cmd

if __name__ == '__main__':
	keys = cmd.keys()
	print('\n'.join(keys))
