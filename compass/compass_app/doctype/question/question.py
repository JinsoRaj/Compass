# Copyright (c) 2025, JinsoRaj and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe import throw, _

class Question(Document):
	def validate(self):
		"""Auto-set weights and validate ranks"""
		if self.options:
			max_weight = len(self.options)
			seen_ranks = set()
			
			for option in self.options:
					# Validate rank
					if option.rank < 1:
						throw(_("Rank must be at least 1"))
					if option.rank > max_weight:
						throw(_("Rank cannot exceed number of options"))
					if option.rank in seen_ranks:
						throw(_("Duplicate rank {} found").format(option.rank))
					seen_ranks.add(option.rank)
					
					# Calculate weight
					option.weight = max_weight - option.rank + 1