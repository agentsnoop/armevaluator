from __future__ import unicode_literals

import json
import base64
import uuid
import hashlib

CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def _base64_(item):
	"""Returns the base64 representation of the input string."""
	return base64.b64encode(item)

def _base64tojson_(item):
	"""Converts a base64 representation to a JSON object."""
	return json.dumps(base64.b64decode(item))

def _base64tostring_(item):
	"""Converts a base64 representation to a string."""
	return base64.b64decode(item)

# def _concat_(*items):
# 	"""Combines multiple string values and returns the concatenated string, or combines multiple arrays and returns the concatenated array."""
# 	is_array = True
# 	result = []
# 	for item in items:
# 		if not isinstance(item, list):
# 			is_array = True
# 		result += item
# 	if not is_array:
# 		result = "".join(result)
# 	return result

# def _contains_(container, item_to_find):
# 	"""
# 	Checks whether an array contains a value, an object contains a key, or a string contains a substring.
# 	The string comparison is case-sensitive. However, when testing if an object contains a key, the comparison is case-insensitive.
# 	"""
# 	if isinstance(container, dict):
# 		return item_to_find.lower() in [key.lower() for key in container.keys()]
# 	return item_to_find in container

def _datauri_(item):
	"""Converts a value to a data URI."""

def _datauritostring_(item):
	"""Converts a data URI formatted value to a string."""

# def _empty_(item):
# 	"""Determines if an array, object, or string is empty."""
# 	return True if len(item) == 0 else False

def _endswith_(item, end):
	"""Determines whether a string ends with a value. The comparison is case-insensitive."""
	return item.endswith(end)

# def _first_(item):
# 	"""Returns the first element of the array, or first character of the string."""
# 	return item[0]

def _format_(fmt, *args):
	"""Creates a formatted string from input values."""
	return "format({fmt})".format(fmt=fmt)

def _guid_(*items):
	"""Creates a value in the format of a globally unique identifier based on the values provided as parameters."""
	# return "guid({items})".format(items=", ".join(items))
	return str(uuid.uuid5(uuid.NAMESPACE_DNS, "".join(items).encode('utf-8')))

def _indexof_(item, search):
	"""Returns the first position of a value within a string. The comparison is case-insensitive."""
	return item.index(search)

# def _last_(item):
# 	"""Returns the last element of the array, or last character of the string."""
# 	return item[-1]

def _lastindexof_(item, search):
	"""Returns the last position of a value within a string. The comparison is case-insensitive."""
	return item[::-1].index(search[::-1])

# def _length_(item):
# 	"""Returns the number of elements in an array, characters in a string, or root-level properties in an object."""
# 	return len(item)

def _newguid_():
	"""Returns a value in the format of a globally unique identifier. This function can only be used in the default value for a parameter."""
	# return "newguid()"
	return str(uuid.uuid4())

def _padleft_(item, length, character=" "):
	"""Returns a right-aligned string by adding characters to the left until reaching the total specified length."""
	return character * (int(length)-len(str(item))) + str(item)

def _replace_(item, old_str, new_str):
	"""Returns a new string with all instances of one string replaced by another string."""
	return item.replace(old_str, new_str)

# def _skip_(item, count):
# 	"""
# 	Returns an array with all the elements after the specified number in the array,
# 	or returns a string with all the characters after the specified number in the string.
# 	"""
# 	return item[count:]

def _split_(item, character):
	"""Returns an array of strings that contains the substrings of the input string that are delimited by the specified delimiters."""
	return item.split(character)

def _startswith_(item, start):
	"""Determines whether a string starts with a value. The comparison is case-insensitive."""
	return item.startswith(start)

def _string_(item):
	"""Converts the specified value to a string."""
	if isinstance(item, (list, dict)):
		return json.dumps(item)
	return str(item)

def _substring_(item, start, end):
	"""Returns a substring that starts at the specified character position and contains the specified number of characters."""
	return item[start:end]

# def _take_(item, count):
# 	"""
# 	Returns an array with the specified number of elements from the start of the array,
# 	or a string with the specified number of characters from the start of the string.
# 	"""
# 	return item[:count]

def _tolower_(item):
	"""Converts the specified string to lower case."""
	return item.lower()

def _toupper_(item):
	"""Converts the specified string to upper case."""
	return item.upper()

def _trim_(item):
	"""Removes all leading and trailing white-space characters from the specified string."""
	return item.strip()

def _uniquestring_(*items):
	"""Creates a deterministic hash string based on the values provided as parameters."""
	# return "uniqueString({items})".format(items=", ".join(items))
	result = ""
	hashed_items = hashlib.sha512()
	for item in items:
		hashed_items.update(item)
	for b in hashed_items.digest():
		result += CHARS[(ord(b) % 62)]
	return result[:13]

def _uri_(*items):
	"""Creates an absolute URI by combining the baseUri and the relativeUri string."""
	return "uri({items})".format(items=", ".join(items))

def _uricomponent_(item):
	"""Encodes a URI."""
	return "uricomponent({item})".format(item=item)

def _uricomponenttostring_(item):
	"""Returns a string of a URI encoded value."""
	return "uricomponenttostring({item})".format(item=item)

def _utcnow_(fmt=None):
	"""
	Returns the current (UTC) datetime value in the specified format.
	If no format is provided, the ISO 8601 (yyyyMMddTHHmmssZ) format is used.
	This function can only be used in the default value for a parameter.
	"""
	if fmt is None:
		fmt = "%Y%m%dT%H%M%SZ"
	return "utcnow({fmt})".format(fmt=fmt)
