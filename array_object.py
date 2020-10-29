from __future__ import unicode_literals

import json
import copy

def _array_(item):
	"""Converts the value to an array."""
	return item if isinstance(item, list) else [item]

def _coalesce_(*items):
	"""Returns first non-null value from the parameters. Empty strings, empty arrays, and empty objects are not null."""
	for item in items:
		if item is not None:
			return item

def _concat_(*items):
	"""Combines multiple arrays and returns the concatenated array, or combines multiple string values and returns the concatenated string."""
	is_array = True
	result = []
	for item in items:
		if not isinstance(item, list):
			is_array = False
			break
		result += item
	if not is_array:
		result = "".join([str(item) for item in items])
	return result

def _contains_(container, item_to_find):
	"""
	Checks whether an array contains a value, an object contains a key, or a string contains a substring.
	The string comparison is case-sensitive. However, when testing if an object contains a key, the comparison is case-insensitive.
	"""
	if isinstance(container, dict):
		return item_to_find.lower() in [key.lower() for key in container.keys()]
	return item_to_find in container

def _createarray_(*items):
	"""Creates an array from the parameters."""
	return items

def _empty_(item):
	"""Determines if an array, object, or string is empty."""
	return True if item and len(item) == 0 else False

def _first_(item):
	"""Returns the first element of the array, or first character of the string."""
	return item[0]

def _intersection_(*items):
	"""Returns a single array or object with the common elements from the parameters."""
	if isinstance(items[0], list):
		try:
			common = set(items[0])
			for arg in items[1:]:
				common.intersection(set(arg))
			return list(common)
		except Exception:
			return []
	elif isinstance(items[0], dict):
		try:
			common = {}
			for k, v in items[0].items():
				for arg in items[1:]:
					if arg.get(k) == v:
						common[k] = v
			return common
		except Exception:
			return {}

def _json_(item):
	"""Returns a JSON object."""
	try:
		if item.lower() == "none":
			item = "null"
		return json.loads(item)
	except Exception as e:
		raise e

def _last_(item):
	"""Returns the last element of the array, or last character of the string."""
	return item[-1]

def _length_(item):
	"""Returns the number of elements in an array, characters in a string, or root-level properties in an object."""
	return len(item)

def _min_(*items):
	"""Returns the minimum value from an array of integers or a comma-separated list of integers."""
	return min(items[0] if len(items) == 1 else min(items))

def _max_(*items):
	"""Returns the maximum value from an array of integers or a comma-separated list of integers."""
	return max(*items)

def _range_(start, count):
	"""Creates an array of integers from a starting integer and containing a number of items."""
	return range(start, start+count+1)

def _skip_(item, count):
	"""
	Returns an array with all the elements after the specified number in the array,
	or returns a string with all the characters after the specified number in the string.
	"""
	return item[count:]

def _take_(item, count):
	"""
	Returns an array with the specified number of elements from the start of the array,
	or a string with the specified number of characters from the start of the string.
	"""
	return item[:count]

def _union_(*items):
	"""Returns a single array or object with all elements from the parameters. Duplicate values or keys are only included once."""
	if isinstance(items[0], list):
		hash_list = []
		try:
			hash_list.append(hash(items[0]))
		except:
			hash_list.append(hash(json.dumps(items[0], sort_keys=True)))

		common = copy.deepcopy(items[0])
		for item in items[1:]:
			try:
				item_hash = hash(item)
			except:
				item_hash = hash(json.dumps(item, sort_keys=True))
			if item_hash not in hash_list:
				hash_list.append(item_hash)
				common += item
		return common

	elif isinstance(items[0], dict):
		common = copy.deepcopy(items[0])
		for item in items[1:]:
			common.update(item)
		return common
	else:
		return list(set(items))

def _exists_(item):
	return item is not None
