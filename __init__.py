# import sys
# import os
# import copy
# import json
# from collections import OrderedDict
#
# from automaton.cloud.azure.resource import Resource
# from automaton.cloud.azure.template.deployment import _parameters_, _variables_
# from automaton.cloud.azure.template.array_object import (
# 	_array_, _coalesce_, _concat_, _contains_, _createarray_, _empty_, _first_, _intersection_,
# 	_json_, _last_, _length_, _max_, _min_, _range_, _skip_, _take_, _union_, _exists_
# )
# from automaton.cloud.azure.template.string import (
# 	_base64_, _base64tojson_, _base64tostring_, _datauri_, _datauritostring_, _endswith_, _format_, _guid_, _indexof_,
# 	_lastindexof_, _newguid_, _padleft_, _replace_, _split_, _startswith_, _string_, _substring_, _tolower_, _toupper_,
# 	_trim_, _uniquestring_, _uri_, _uricomponent_, _uricomponenttostring_, _utcnow_
# )
# from automaton.cloud.azure.template.resource import (
# 	PROVIDERS,
# 	_extensionresourceid_, _listkeys_, _providers_, _reference_, _resourceid_,
# 	_subscriptionresourceid_, _tenantresourceid_, _validate_uuid
# )
# from automaton.cloud.azure.template.comparison import _equals_, _greater_, _greaterorequals, _less_, _lessorequals_
# from automaton.cloud.azure.template.logic import _and_, _bool_, _if_, _not_, _or_
# from automaton.cloud.azure.template.numeric import _add_, _copy_index_, _div_, _float_, _int_, _mod_, _mul_, _sub_
#
# def _copyindex_(obj):
# 	return "copyIndex({obj})".format(obj=obj)
#
# class Template(object):
# 	def __init__(self, arm, resource_group=None, subscription_id=None):
# 		self.arm 		= arm
#
# 		self.data		= None
# 		self.path		= None
# 		self.input_path	= None
# 		self.input_data = None
#
# 		self.resource_group_name 	= resource_group
# 		self.subscription_id 		= subscription_id
# 		self.resource_group			= None
# 		self.subscription			= None
#
# 		self.input_parameters 		= None
# 		self.parameters				= None
# 		self.variables				= None
# 		self.resources				= None
# 		self.all_resources			= []
#
# 	def load_environment(self, resource_group=None, subscription_id=None):
# 		if resource_group:
# 			self.resource_group_name = resource_group
# 		if subscription_id:
# 			self.subscription_id = subscription_id
#
# 		self.arm.subscription_id = self.subscription_id
#
# 		resource_group = self.arm.get_resource_group_by_name(self.resource_group_name)
# 		if not resource_group:
# 			tags = self._parameters_("tags")
# 			location = self._parameters_("location")
# 			print("Resource Group [{name}] not found. Creating at [{location}]...".format(name=self.resource_group_name, location=location))
# 			self.arm.create_resource_group(self.resource_group_name, location, tags=tags)
# 			resource_group = self.arm.get_resource_group_by_name(self.resource_group_name)
#
# 		self.resource_group = {
# 			"id": resource_group.id,
# 			"name": resource_group.name,
# 			"type": "Microsoft.Resources/resourceGroups",
# 			"location": resource_group.location,
# 			"managedBy": resource_group.managed_by,
# 			"tags": resource_group.tags,
# 			"properties": {
# 				"provisioningState": resource_group.properties["provisioning_state"]
# 			}
# 		}
#
# 		subscription = self.arm.subscription
# 		self.subscription = {
# 			"id": subscription.id,
# 			"subscriptionId": subscription.subscription_id,
# 			"tenantId": self.arm.tenant_id,
# 			"displayName": subscription.display_name
# 		}
#
# 	def load_parameters(self, path):
# 		if not os.path.exists(path):
# 			print("Parameters path does not exist [{path}]".format(path=path))
# 			return False
#
# 		self.input_path = path
# 		with open(path) as fd:
# 			self.input_data 		= json.load(fd, object_pairs_hook=OrderedDict)
# 			self.input_parameters 	= copy.deepcopy(self.input_data.get("parameters"))
#
# 	def load_template(self, path):
# 		if not os.path.exists(path):
# 			print("Template path does not exist [{path}]".format(path=path))
# 			return False
#
# 		self.path = path
# 		with open(path) as fd:
# 			self.data 	= json.load(fd, object_pairs_hook=OrderedDict)
# 			self.resources 		= copy.deepcopy(self.data.get("resources"))
# 			self.variables 		= copy.deepcopy(self.data.get("variables"))
# 			self.parameters		= copy.deepcopy(self.data.get("parameters"))
#
# 	def reload(self):
# 		self.load_parameters(self.input_path)
# 		self.load_template(self.path)
#
# 	def whatif(self):
# 		if self.parameters:
# 			self.parameters = self._evaluate_dict(self.parameters, obj_name="parameters")
# 		if self.variables:
# 			self.variables = self._evaluate_dict(self.variables, obj_name="variables")
#
# 		expanded_resources = []
# 		self.all_resources = []
# 		for res in self.resources:
# 			if "copy" in res:
# 				res = self._evaluate_copy(res)
# 				expanded_resources += res
# 				self.all_resources += res
# 			else:
# 				res = self._evaluate_dict(res)
#
# 				condition = res.pop("condition", True)
# 				if condition:
# 					expanded_resources.append(res)
#
# 				self.all_resources.append(res)
# 		self.resources = expanded_resources
#
# 	def _evaluate_copy_array(self, obj, parent):
# 		for subobj in obj:
# 			copy_name = subobj.get("name")
# 			parent[copy_name] = self._evaluate_copy(subobj)
# 		return parent
#
# 	def _evaluate_copy(self, obj):
# 		data = []
#
# 		copy_data = self._evaluate_dict(obj.pop("copy", obj))
# 		copy_data.pop("mode", None)
# 		copy_data.pop("batchSize", None)
# 		name = copy_data.pop("name", None)
# 		count = int(copy_data.pop("count", 0))
#
# 		if count == 0:
# 			return data
#
# 		copy_input = copy_data.pop("input", None)
# 		for index in range(count):
# 			copy_obj = copy.deepcopy(copy_input) if copy_input else copy.deepcopy(obj)
# 			res = self._evaluate_dict(copy_obj, index, name)
#
# 			# TODO: Only target resources
# 			if res.pop("condition", True):
# 				data.append(res)
#
# 		return data
#
# 	def _evaluate_dict(self, obj, copy_index=None, copy_name=None, obj_name=None):
# 		deferred_keys = []
#
# 		keys = obj.keys()
# 		for k in keys:
# 			v = obj[k]
# 			if k == "copy":
# 				self._evaluate_copy_array(v, obj)
# 				continue
# 			elif k == "reference":
# 				v = self._evaluate_reference(v)
# 				obj.pop(k, None)
# 				obj["value"] = v
# 				continue
#
# 			new_key = self._evaluate_string(k, copy_index, copy_name)
# 			if new_key != k:
# 				obj.pop(k, None)
# 				k = new_key
#
# 			if isinstance(v, dict):
# 				v = self._evaluate_dict(v, copy_index, copy_name)
#
# 				# TODO: Only target resources
# 				if not v.pop("condition", True):
# 					continue
#
# 			elif isinstance(v, list):
# 				v = self._evaluate_list(v, copy_index, copy_name)
# 			elif isinstance(v, (str, unicode)):
# 				try:
# 					v = self._evaluate_string(v, copy_index, copy_name)
# 				except Exception:
# 					deferred_keys.append(k)
# 					continue
# 			obj[k] = v
#
# 		for k in deferred_keys:
# 			v = obj[k]
# 			if isinstance(v, (str, unicode)):
# 				v = self._evaluate_string(v, copy_index, copy_name)
# 			obj[k] = v
#
# 		return obj
#
# 	def _evaluate_list(self, obj, copy_index=None, copy_name=None):
# 		for index, v in enumerate(obj):
# 			if isinstance(v, dict):
# 				v = self._evaluate_dict(v, copy_index, copy_name)
#
# 				# TODO: Only target resources
# 				if not v.pop("condition", True):
# 					continue
#
# 			elif isinstance(v, list):
# 				v = self._evaluate_list(v, copy_index, copy_name)
# 			elif isinstance(v, (str, unicode)):
# 				v = self._evaluate_string(v, copy_index, copy_name)
# 			obj[index] = v
# 		return obj
#
# 	def _evaluate_string(self, obj, copy_index=None, copy_name=None):
# 		if "copyIndex(" in obj:
# 			if copy_index is None:
# 				return obj
# 			obj = self._evaluate_copy_index(obj, copy_index, copy_name)
#
# 		if obj.startswith("[") and obj.endswith("]") and not obj.startswith("[["):
# 			result = self._evaluate_value(obj)
# 			result = self._evaluate_object(*result) if len(result) > 1 else result[0]
# 			return result
# 		return obj
#
# 	def _evaluate_copy_index(self, obj, copy_index, copy_name=None):
# 		# Determine copy_offset
# 		start = obj.index("copyIndex(") + 10
# 		end = obj.index(")", start)
#
# 		while obj[start:end].count("(") != obj[start:end].count(")"):
# 			end += 1
#
# 		result = self._evaluate_value("[{value}]".format(value=obj[start:end]))
# 		if result:
# 			result = self._evaluate_object(*result) if len(result) > 1 else result[0]
# 			obj = obj[:start] + str(result) + obj[end:]
# 		else:
# 			result = ""
#
# 		copy_params = result.split(",")
# 		# copy_params = self._split(str(result), ",")
# 		# copy_params = obj[start:end].split(",")
#
# 		if len(copy_params) == 2:
# 			copy_offset = int(copy_params[1].strip())
# 		# elif copy_params[0].strip() and not copy_params[0] == copy_name:
# 		elif copy_params[0].strip() and not copy_params[0] == "'{name}'".format(name=copy_name):
# 			copy_offset = int(copy_params[0].strip())
# 		else:
# 			copy_offset = None
#
# 		obj = obj.replace("copyIndex()", str(copy_index))
# 		obj = obj.replace("copyIndex('{name}')".format(name=copy_name), str(copy_index))
# 		if copy_offset is not None:
# 			obj = obj.replace("copyIndex({offset})".format(offset=copy_offset), str(copy_index + copy_offset))
# 			obj = obj.replace("copyIndex('{name}', {offset})".format(name=copy_name, offset=copy_offset), str(copy_index + copy_offset))
# 		return obj
#
# 	@staticmethod
# 	def _evaluate_object(obj, helper):
# 		accesses = helper.lstrip(".").split(".")
#
# 		for access in accesses:
# 			if access.startswith("["):
# 				end = access.index("]")
# 				index = int(access[1:end])
# 				obj = obj[index]
# 			else:
# 				if "[" in access:
# 					end = access.index("[")
# 					key = access[:end]
# 					obj = obj[key]
# 					access = access[end:]
# 					if access.startswith("["):
# 						end = access.index("]")
# 						index = int(access[1:end])
# 						obj = obj[index]
# 				elif obj is not None:
# 					if isinstance(obj, Resource):
# 						obj = getattr(obj, access)
# 					else:
# 						obj = obj.get(access) if hasattr(obj, "get") else obj[access]
# 		return obj
#
# 	def _evaluate_reference(self, obj):
# 		value = None
# 		if "keyVault" in obj:
# 			resource_data = self.arm.parse_id(obj["keyVault"]["id"])
# 			if resource_data["subscription"] != self.subscription_id:
# 				self.arm.subscription_id = resource_data["subscription"]
# 			rg = self.arm.get_resource_group_by_name(resource_data["resource_group"])
# 			kv = rg.get_key_vault(resource_data["resource_name"])
#
# 			if kv and "secretName" in obj:
# 				try:
# 					value = kv.get_secret(obj["secretName"]).value
# 				except Exception as e:
# 					value = str(e).split("\n")[0].strip()
# 			self.arm.subscription_id = self.subscription_id
# 		return value
#
# 	def _evaluate_value(self, value):
# 		word = ""
# 		stack = []
# 		quote_stack = []
# 		for c in value[1:-1]:
# 			if c not in ['(', ')', ',']:
# 				if c in ["'"]:
# 					quote_stack.pop() if quote_stack else quote_stack.append(c)
# 				word += c
# 			elif c == ',':
# 				if not quote_stack:
# 					word = word.strip(",").strip()
# 					if word:
# 						stack.append(word.strip("'"))
# 					word = ""
# 				else:
# 					word += c
# 			elif c == '(':
# 				word = word.strip(",").strip()
# 				stack.append(word.strip("'"))
# 				stack.append(c)
# 				word = ""
# 			elif c == ')':
# 				func = []
# 				word = word.strip(",").strip()
# 				if word:
# 					func.insert(0, word.strip("'"))
# 				word = ""
# 				p = stack.pop()
# 				while p != '(':
# 					func.insert(0, p)
# 					p = stack.pop()
# 				p = stack.pop()
# 				func.insert(0, p.lower())
#
# 				# Compute array access
# 				resolved_func = [func[0]]
# 				index = 1
# 				while index < len(func):
# 					if index < len(func)-1 and isinstance(func[index+1], (str, unicode)) and func[index+1].startswith("["):
# 						resolved_func.append(self._evaluate_object(func[index], func[index+1]))
# 						index += 2
# 					else:
# 						resolved_func.append(func[index])
# 						index += 1
#
# 				result = self.call(*resolved_func)
# 				stack.append(result)
# 		if word:
# 			stack.append(word)
# 		return stack
#
# 	def _parameters_(self, key):
# 		value = self.input_parameters.get(key)
# 		if value:
# 			return value.get("value")
# 		value = self.parameters.get(key)
# 		if value:
# 			return value.get("defaultValue")
#
# 	def call(self, name, *args):
# 		if name == "parameters":
# 			return self._parameters_(args[0])
# 		elif name == "variables":
# 			return self.variables.get(args[0])
# 		elif name == "resourcegroup":
# 			return self.resource_group
# 		elif name == "subscription":
# 			return self.subscription
#
# 		resolved_args = []
# 		index = 0
# 		while index < len(args):
# 			arg = args[index]
# 			next_arg = args[index+1] if index+1 < len(args) else None
# 			resolved_arg = arg
#
# 			if next_arg and isinstance(next_arg, (str, unicode)) and next_arg[0] in ["[", "."]:
# 				if isinstance(arg, (list, dict)):
# 					resolved_arg = self._evaluate_object(arg, next_arg)
# 					index += 1
#
# 			resolved_args.append(resolved_arg)
# 			index += 1
#
# 		kwargs = {}
# 		if name == "resourceid":
# 			kwargs.update({"subscription_id": self.subscription_id, "resource_group_name": self.resource_group_name})
# 		elif name == "reference":
# 			kwargs.update({"arm": self.arm})
#
# 		# print "resolved args:", name, resolved_args
# 		func = getattr(sys.modules[__name__], "_{name}_".format(name=name.lower()))
# 		return func(*resolved_args, **kwargs)
#
# 	def _split(self, buff, char=" "):
# 		results = []
# 		quote_stack = []
# 		result = ""
# 		for c in buff:
# 			if c in ["'"]:
# 				if quote_stack and quote_stack[-1] == c:
# 					quote_stack.pop()
# 				else:
# 					quote_stack.append(c)
# 				continue
#
# 			if c == char and not quote_stack:
# 				results.append(result)
# 				result = ""
# 				continue
#
# 			result += c
# 		results.append(result)
# 		return results