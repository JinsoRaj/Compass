# # compass/api.py
# import frappe
# from frappe import _

# @frappe.whitelist()
# def get_options_for_display(question, txt=None):
#     """Return options with proper formatting for dropdown"""
#     if not question:
#         return []

#     filters = {"parent": question}
#     if txt:
#         filters["option_text"] = ["like", f"%{txt}%"]

#     options = frappe.get_all(
#         "Question Option",
#         filters=filters,
#         fields=["name", "option_text"],
#         order_by="idx"
#     )

#     return [{"value": opt["name"], "label": opt["option_text"]} for opt in options]