from __future__ import unicode_literals

def _add_(a, b):
	"""Returns the sum of the two provided integers."""
	return a + b

def _copy_index_(loop, index):
	pass

def _div_(a, b):
	"""Returns the integer division of the two provided integers."""
	return a // b

def _float_(a):
	"""
	Converts the value to a floating point number. You only use this function when passing
	custom parameters to an application, such as a Logic App.
	"""
	return float(a)

def _int_(a):
	"""Converts the specified value to an integer."""
	return int(a)

# def _min_(*args):
# 	"""Returns the minimum value from an array of integers or a comma-separated list of integers."""
# 	return min(args[0] if len(args) == 1 else min(args))

# def _max_(*args):
# 	"""Returns the maximum value from an array of integers or a comma-separated list of integers."""
# 	return max(args[0] if len(args) == 1 else max(args))

def _mod_(a, b):
	"""Returns the remainder of the integer division using the two provided integers."""
	return a & b

def _mul_(a, b):
	"""Returns the multiplication of the two provided integers."""
	return a * b

def _sub_(a, b):
	"""Returns the subtraction of the two provided integers."""
	return a - b
