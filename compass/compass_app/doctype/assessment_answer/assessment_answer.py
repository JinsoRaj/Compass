# Copyright (c) 2025, JinsoRaj and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class AssessmentAnswer(Document):
	pass


#custom
@frappe.whitelist()
def get_question_options(question):
    """Get options for the selected question with proper debugging"""
    try:
        # Debug: Print the received question
        frappe.logger().debug(f"Received question: {question}")
        
        if not question:
            return []
            
        # Method 1: Using Frappe's get_doc (most reliable)
        question_doc = frappe.get_doc("Question", question)
        options = [d.name for d in question_doc.options]
        
        # Debug: Print the found options
        frappe.logger().debug(f"Options found: {options}")
        
        # Method 2: Alternative SQL query if above doesn't work
        if not options:
            options = frappe.db.sql("""
                SELECT qo.name 
                FROM `tabQuestion Option` qo
                WHERE qo.parenttype = 'Question' 
                AND qo.parent = %s
                ORDER BY qo.idx
            """, question, as_dict=True)
            options = [d.name for d in options]
            frappe.logger().debug(f"SQL options: {options}")
        
        return options
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Failed to get question options")
        frappe.throw(_("Failed to load options. Please refresh and try again."))