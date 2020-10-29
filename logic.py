from __future__ import unicode_literals

def _and_(*args):
	result = True
	for arg in args:
		result &= arg
	return result

def _bool_(item):
	"""Converts the parameter to a boolean."""
	return bool(item)

def _if_(a, b, c):
	"""Returns a value based on whether a condition is true or false."""
	return b if a else c

def _not_(item):
	"""Converts boolean value to its opposite value."""
	return not item

def _or_(*args):
	"""Checks whether any parameter value is true."""
	result = False
	for arg in args:
		result |= arg
	return result
