from __future__ import unicode_literals

def _equals_(a, b):
	"""Checks whether two values equal each other."""
	if isinstance(a, list):
		if not isinstance(b, list):
			return False

		if len(a) != len(b):
			return False
		for index, item in enumerate(a):
			if item != b[index]:
				return False
		return True

	if isinstance(a, dict):
		if not isinstance(b, dict):
			return False

		if len(a) != len(b):
			return False
		for k, v in a.items():
			if k not in b or v != b[k]:
				return False
		return True

	return a == b

def _less_(a, b):
	"""Checks whether the first value is less than the second value."""
	return a < b

def _lessorequals_(a, b):
	"""Checks whether the first value is less than or equal to the second value."""
	return a <= b

def _greater_(a, b):
	"""Checks whether the first value is greater than the second value."""
	return a > b

def _greaterorequals(a, b):
	"""Checks whether the first value is greater than or equal to the second value."""
	return a >= b
