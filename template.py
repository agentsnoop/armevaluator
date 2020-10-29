from __future__ import unicode_literals

import sys
import os
import copy
import json
from collections import OrderedDict

from automaton.cloud.azure.evaluation.base import Base

class Template(Base):
	def __init__(self, arm, resource_group=None, subscription_id=None):
		super(Template, self).__init__(arm, resource_group, subscription_id)
		self.input_parameters 		= None
		self.resources				= None
		self.all_resources			= []

	def load_template(self, path):
		if not os.path.exists(path):
			print("Template path does not exist [{path}]".format(path=path))
			return False

		self.path = path
		with open(path) as fd:
			self.data 	= json.load(fd, object_pairs_hook=OrderedDict)
			self.resources 		= copy.deepcopy(self.data.get("resources", {}))
			self.variables 		= copy.deepcopy(self.data.get("variables", {}))
			self.parameters		= copy.deepcopy(self.data.get("parameters", {}))

	def reload(self):
		self.load_parameters(self.input_path)
		self.load_template(self.path)

	def whatif(self):
		if self.input_parameters:
			self.input_parameters = self._evaluate_dict(self.input_parameters)
		if self.parameters:
			self.parameters = self._evaluate_dict(self.parameters, obj_name="parameters")
		if self.variables:
			self.variables = self._evaluate_dict(self.variables, obj_name="variables")
		expanded_resources = []
		self.all_resources = []
		for res in self.resources:
			if "copy" in res:
				res = self._evaluate_copy(res)
				self.resources += res
				self.all_resources += res
			else:
				res = self._evaluate_dict(res)

				condition = res.pop("condition", True)
				if condition:
					expanded_resources.append(res)

				self.all_resources.append(res)
		self.resources = expanded_resources

	def show(self, index=None):
		if index is not None:
			print(json.dumps(self.resources[index], indent=2))
		else:
			for resource in self.resources:
				print(json.dumps(resource, indent=2))

	def show_all(self, index=None):
		if index is not None:
			print(json.dumps(self.all_resources[index], indent=2))
		else:
			for resource in self.all_resources:
				print(json.dumps(resource, indent=2))