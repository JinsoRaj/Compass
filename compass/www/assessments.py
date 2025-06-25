import frappe

def get_context(context):
    context.assessments = frappe.get_all("Assessment", fields=["name", "assessment_name", "description", "time_required"])
    return context
