# Copyright (c) 2025, JinsoRaj and contributors
# For license information, please see license.txt
# assessment_response.py
import frappe
from frappe.model.document import Document

class AssessmentResponse(Document):
    def before_save(self):
        # Server-side weight calculation
        for answer in self.answers:
            if answer.question and answer.selected_option:
               option_data = self.get_option_details(answer.question, answer.selected_option)
               answer.weight = option_data.get("weight", 0)
               answer.selected_option_text = option_data.get("option_text", "")
        
        self.total_score = sum(answer.weight for answer in self.answers if answer.weight)
        self.max_possible_score = self.calculate_max_possible_score()
        self.percentage_score = (self.total_score / self.max_possible_score * 100) if self.max_possible_score else 0
        self.current_scale = self.get_current_scale()

    def calculate_max_possible_score(self):
        max_score = 0
        questions = {answer.question for answer in self.answers}
        for question_name in questions:
            question = frappe.get_doc("Question", question_name)
            if question.options:
                max_score += max((option.weight for option in question.options if option.weight), default=0)
        return max_score

    def get_current_scale(self):
        assessment = frappe.get_doc("Assessment", self.assessment)
        for scale in assessment.scales:
            if scale.min_score <= self.percentage_score <= scale.max_score:
                return scale.scale_name
        return "Undefined"

    @staticmethod
    def get_option_details(question, option_name):
          result = frappe.db.get_value(
				"Question Option",
				{"parent": question, "name": option_name},
				["weight", "option_text"],
				as_dict=True
			)
          return result or {"weight": 0, "option_text": ""}