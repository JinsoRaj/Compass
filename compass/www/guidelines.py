import frappe

def get_context(context):
    assessment_name = frappe.form_dict.assessment
    context.assessment = assessment_name
    return context