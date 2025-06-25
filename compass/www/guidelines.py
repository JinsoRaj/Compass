import frappe


def get_context(context):
    # Get assessment name from URL parameters
    assessment_name = frappe.form_dict.get("assessment")
    
    if not assessment_name:
        frappe.throw("Invalid assessment URL", frappe.PermissionError)

    # Fetch assessment details
    context.assessment = frappe.get_doc("Assessment", assessment_name)

    #Add validation
    if not context.assessment:
        frappe.throw("Assessment not found", frappe.DoesNotExistError)

    return context