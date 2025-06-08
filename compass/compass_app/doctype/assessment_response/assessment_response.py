# Copyright (c) 2025, JinsoRaj and contributors
# For license information, please see license.txt
# assessment_response.py
import frappe
from frappe.model.document import Document
from collections import defaultdict

class AssessmentResponse(Document):
    def before_save(self):
        # Server-side weight calculation
        for answer in self.answers:
            if answer.question and answer.selected_option:
               option_data = self.get_option_details(answer.question, answer.selected_option)
               answer.weight = option_data.get("weight", 0)
               answer.selected_option_text = option_data.get("option_text", "")
        
        # Calculate pillar scores and set pillar fields
        pillar_data = self.calculate_pillar_scores()
        self.set_pillar_fields(pillar_data)
        
        # Calculate overall scores
        self.total_score = sum(answer.weight for answer in self.answers if answer.weight)
        self.max_possible_score = self.calculate_max_possible_score()
        self.percentage_score = (self.total_score / self.max_possible_score * 100) if self.max_possible_score else 0
        self.current_scale, self.scale_description = self.get_current_scale()

    def calculate_pillar_scores(self):
        """Calculate scores and percentages for each pillar"""
        pillar_scores = defaultdict(lambda: {'total': 0, 'max': 0, 'questions': set()})
        
        # Group scores by pillar
        for answer in self.answers:
            if not answer.pillar:
                continue
                
            pillar = answer.pillar
            pillar_scores[pillar]['total'] += answer.weight
            pillar_scores[pillar]['questions'].add(answer.question)
        
        # Calculate max possible scores for each pillar
        for pillar, data in pillar_scores.items():
            max_score = 0
            for question_name in data['questions']:
                question = frappe.get_doc("Question", question_name)
                if question.options:
                    max_score += max((option.weight for option in question.options if option.weight), default=0)
            data['max'] = max_score
            data['percentage'] = (data['total'] / data['max'] * 100) if data['max'] else 0
        
        return pillar_scores

    def set_pillar_fields(self, pillar_data):
        """Set pillar text and score fields based on calculated data"""
        # Reset existing fields
        for i in range(1, 4):
            setattr(self, f"pillar_{i}_text", None)
            setattr(self, f"pillar_{i}_score", None)
        
        # Set fields for up to 3 pillars
        for i, pillar in enumerate(sorted(pillar_data.keys())[:3], start=1):
            data = pillar_data[pillar]
            setattr(self, f"pillar_{i}_text", pillar)
            setattr(self, f"pillar_{i}_score", f"{data['percentage']:.1f}%")

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
                return scale.scale_name, scale.scale_description  # Return both values as a tuple
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