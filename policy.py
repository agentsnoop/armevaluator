from __future__ import unicode_literals

import os
import re
import json
import copy
import fnmatch
from collections import OrderedDict

import yaml

from automaton.cloud.azure.evaluation.base import Base

class Policy(Base):
	def __init__(self, arm, resource_group, subscription_id):
		super(Policy, self).__init__(arm, resource_group, subscription_id)
		self.target			= False
		self.effect			= None
		self.param_data		= None
		self.policy_rule 	= None
		self.resource		= None
		self.field			= None
		self.obj			= None
		self.results		= []

	def load_policy(self, path, values_path=None):
		if not os.path.exists(path):
			print("Template path does not exist [{path}]".format(path=path))
			return False

		try:
			self.path = path
			with open(path) as fd:
				self.data = json.load(fd, object_pairs_hook=OrderedDict)
				self.policy_rule = copy.deepcopy(self.data)
				# self.policy_rule = copy.deepcopy(self.data.get("policyRule"))
				# self.variables = copy.deepcopy(self.data.get("variables"))
				# self.parameters = copy.deepcopy(self.data.get("parameters"))
		except ValueError:
			print("Error loading [{path}]".format(path=path))

		parameters_path = path.replace(".json", ".param.json")
		if os.path.exists(parameters_path):
			# print("Loading Parameters from [{path}]".format(path=path))
			with open(parameters_path) as fd:
				self.param_data = json.load(fd, object_pairs_hook=OrderedDict)
				self.parameters = copy.deepcopy(self.param_data)

			if values_path and os.path.exists(values_path):
				with open(values_path) as fd:
					values = yaml.load(fd, Loader=yaml.FullLoader)
					for k, v in values:
						self.parameters[k]["defaultValue"] = v

			exclusions_path = path.replace(".json", ".exclusions.yml")
			if os.path.exists(exclusions_path):
				with open(exclusions_path) as fd:
					exclusions = yaml.load(fd, Loader=yaml.FullLoader)
					for k, v in exclusions.items():
						if "defaultValue" in self.parameters[k]:
							self.parameters[k]["defaultValue"] += v
						else:
							self.parameters[k]["defaultValue"] = v
		return True

	def whatif(self):
		if self.parameters:
			self.parameters = self._evaluate_dict(self.parameters, obj_name="parameters")
		if self.variables:
			self.variables = self._evaluate_dict(self.variables, obj_name="variables")

	def audit(self, resource):
		self.results 	= []
		self.resource 	= resource
		self.target 	= False
		self.effect		= None
		try:
			policy_rule = copy.deepcopy(self.policy_rule)
			policy_rule = self._evaluate_dict(policy_rule)
			success = self.evaluate_if(policy_rule["if"])
			if success:
				self.effect = self.policy_rule["then"].get("effect")
				return self.effect
		except Exception as e:
			# print("Skipping {resource}".format(resource=resource.get("type")))
			pass

	def evaluate_if(self, condition):
		for k, v in condition.items():
			if k.lower() == "count":
				return self.evaluate_count(**condition)
			if k.lower() == "field":
				return self.evaluate_field(**condition)
			if k.lower() == "value":
				return self.evaluate_value(**condition)

			if k.lower() == "anyof":
				return self.evaluate_anyof(v)
			if k.lower() == "allof":
				return self.evaluate_allof(v)
			if k.lower() == "not":
				return not self.evaluate_not(v)
			if k.lower() == "if":
				return self.evaluate_if(v)
		return True

	def evaluate_not(self, condition):
		if "count" in condition:
			return not self.evaluate_count(**condition)
		if "field" in condition:
			return not self.evaluate_field(**condition)
		if "value" in condition:
			return not self.evaluate_value(**condition)

		if "allOf" in condition:
			return not self.evaluate_allof(condition["allOf"])
		if "anyOf" in condition:
			return not self.evaluate_anyof(condition["anyOf"])
		if "not" in condition:
			return not self.evaluate_not(condition["not"])
		return False

	def evaluate_allof(self, conditions):
		for condition in conditions:
			if not isinstance(condition, dict):
				continue

			if "count" in condition:
				if not self.evaluate_count(**condition):
					return False
			if "field" in condition:
				if not self.evaluate_field(**condition):
					return False
			if "value" in condition:
				if not self.evaluate_value(**condition):
					return False

			if "allOf" in condition:
				if not self.evaluate_allof(condition["allOf"]):
					return False
			if "anyOf" in condition:
				if not self.evaluate_anyof(condition["anyOf"]):
					return False
			if "not" in condition:
				if not self.evaluate_not(condition["not"]):
					return False
		return True

	def evaluate_anyof(self, conditions):
		for condition in conditions:
			if not isinstance(condition, dict):
				continue

			if "count" in condition:
				if self.evaluate_count(**condition):
					return True
			if "field" in condition:
				if self.evaluate_field(**condition):
					return True
			if "value" in condition:
				if self.evaluate_value(**condition):
					return True

			if "allOf" in condition:
				if self.evaluate_allof(condition["allOf"]):
					return True
			if "anyOf" in condition:
				if self.evaluate_anyof(condition["anyOf"]):
					return True
			if "not" in condition:
				if self.evaluate_not(condition["not"]):
					return True
		return False

	def evaluate_count(self, count, **kwargs):
		field = count["field"]
		if "[*]" not in field:
			return False

		values = self._evaluate_alias(field)
		where = count.get("where")
		if not where:
			return self.evaluate_value(str(len(values)), **kwargs)

		self.field = field
		result = 0
		for value in values:
			self.obj = value
			if self.evaluate_where(where):
				result += 1

		self.field 	= None
		self.obj 	= None
		return self.evaluate_value(str(result), **kwargs)

	def evaluate_where(self, condition):
		for k, v in condition.items():
			if k.lower() == "field":
				return self.evaluate_field(**condition)
			if k.lower() == "value":
				return self.evaluate_value(**condition)

			if k.lower() == "anyof":
				return self.evaluate_anyof(v)
			if k.lower() == "allof":
				return self.evaluate_allof(v)
			if k.lower() == "not":
				return not self.evaluate_not(v)
			if k.lower() == "if":
				return self.evaluate_if(v)
		return True

	def evaluate_field(self, field, **kwargs):
		original_field = field
		if self.field:
			field = field.replace(self.field, "").strip(".")

		success = True
		if "[*]" in field:
			values = self._evaluate_alias(field)
			for value in values:
				success &= self.evaluate_value(value, field=original_field, **kwargs)
		else:
			value = self._evaluate_field(field)
			if field == "location":
				value = value.replace(" ", "").strip().lower()
			if field == "name":
				value = value.split("/")[-1]
			success = self.evaluate_value(value, field=original_field, **kwargs)

			# Keep track of "targeted" resource
			# if field == "type":
			# 	print self.resource.get("type"), value, success, self.target
			if field == "type" and success:
				self.target = True

		return success

	def evaluate_value(self, value, field=None, **kwargs):
		if field and isinstance(value, (str, unicode)) and value.startswith("[") and value.endswith("]") and not value.startswith("[["):
			value = self._evaluate_value(value)
			value = self._evaluate_object(*value) if len(value) > 1 else value[0]
		if isinstance(value, bool):
			value = str(value).lower()

		success = False
		if "equals" in kwargs:
			success = str(value).lower() == str(kwargs["equals"]).lower()
		elif "notEquals" in kwargs:
			success = str(value).lower() != str(kwargs["notEquals"]).lower()
		elif "less" in kwargs:
			success = int(value) < int(kwargs["less"])
		elif "lessOrEquals" in kwargs:
			success = int(value) <= int(kwargs["lessOrEquals"])
		elif "greater" in kwargs:
			success = int(value) > int(kwargs["greater"])
		elif "greaterOrEquals" in kwargs:
			success = int(value) >= int(kwargs["greaterOrEquals"])
		elif "exists" in kwargs:
			success = (value is not None) == kwargs["exists"]
		elif "in" in kwargs:
			# container = kwargs["in"]
			# if not container:
			# 	container = []
			# if isinstance(container, list):
			# 	container = [str(v).lower() for v in container]
			# success = str(value).lower() in container
			success = self._in_(value, kwargs.get("in", []))
		elif "notIn" in kwargs:
			# container = kwargs["notIn"]
			# if not container:
			# 	container = []
			# if isinstance(container, list):
			# 	container = [str(v).lower() for v in container]
			# success = str(value).lower() not in container
			success = not self._in_(value, kwargs.get("notIn", []))
		elif "contains" in kwargs:
			# container = kwargs["contains"]
			# if not container:
			# 	container = []
			# success = str(value).lower() in [str(v).lower() for v in container.values()]
			success = self._contains_(value, kwargs.get("contains", {}).values())
		elif "notContains" in kwargs:
			# container = kwargs["notContains"]
			# if not container:
			# 	container = {}
			# success = str(value).lower() not in [str(v).lower() for v in container.values()]
			success = not self._contains_(value, kwargs.get("notContains", {}).values())
		elif "containsKey" in kwargs:
			# container = kwargs["containsKey"]
			# if not container:
			# 	container = {}
			# success = value in container
			success = self._contains_(value, kwargs.get("containsKey", {}).keys())
		elif "notContainsKey" in kwargs:
			# container = kwargs["notContainsKey"]
			# if not container:
			# 	container = {}
			# success = value not in container
			success = not self._contains_(value, kwargs.get("notContainsKey", {}).keys())
		elif "like" in kwargs:
			success = self._like_(value, kwargs["like"])
		elif "notLike" in kwargs:
			success = not self._like_(value, kwargs["notLike"])
		# if "match" in kwargs:
		#  return value == kwargs["match"]
		# if "matchInsensitively" in kwargs:
		#  return value == kwargs["matchInsensitively"]
		# if "notMatch" in kwargs:
		#  return value == kwargs["notMatch"]
		# if "notMatchInsensitively" in kwargs:
		#  return value == kwargs["notMatchInsensitively"]

		op = list(kwargs.keys())[0]
		result = {
			"field": field,
			"value": value,
			"expected": kwargs.get(op),
			"operator": op,
			"success": success
		}
		self.results = [result]
		# self.results.append(result)
		return success

	def call(self, name, *args):
		if name == "field":
			if "[*]" in args[0]:
				return self._evaluate_alias(args[0])
			return self._evaluate_field(args[0])

		return super(Policy, self).call(name, *args)

	@staticmethod
	def _in_(value, values):
		if not values:
			values = []
		if isinstance(values, list):
			values = [str(v).lower() for v in values]
		return str(value).lower() in values

	@staticmethod
	def _contains_(value, values):
		if not values:
			values = {}
		return str(value).lower() in [str(v).lower() for v in values]

	@staticmethod
	def _like_(needle, haystack):
		regex = fnmatch.translate(haystack.lower())
		reobj = re.compile(regex)
		return reobj.match(needle.lower()) is not None

	def _evaluate_alias(self, field):
		aliases = field.split("[*]")
		items = self._evaluate_field(aliases[0])
		field_path = aliases[1].strip().lstrip(".").split(".") if aliases[1] else []

		values = self._get_value_from_field(field_path, items)
		return values

	def _evaluate_field(self, field):
		obj = self.obj
		if obj is None:
			obj = self.resource

		index = None
		field = field.split("/")[-1]
		if "[" in field and "]" in field:
			field, index = field.rstrip("]").split("[")
		field_path = field.split(".")

		value = self._get_value_from_field(field_path, obj)
		if index:
			value = value.get(index)
		return value

	@staticmethod
	def _get_value_from_field(field_path, items):
		is_list = True
		if not isinstance(items, list):
			is_list = False
			items = [items]

		values = []
		for item in items:
			value = item
			for sub_field in field_path:
				if not isinstance(value, dict):
					value = None
					break
				value = value.get(sub_field)
			values.append(value)

		if any(values):
			return values if is_list else values[0]

		values = []
		for item in items:
			value = item.get("properties")
			for sub_field in field_path:
				if not isinstance(value, dict):
					value = None
					break
				value = value.get(sub_field)
			values.append(value)
		return values if is_list else values[0]
