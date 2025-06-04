# # compass/api.py
import frappe
import json
from frappe import _

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



@frappe.whitelist(allow_guest=True)
def submit_assessment_response(assessment, responses):
    # Create new response document
    response = frappe.new_doc("Assessment Response")
    response.assessment = assessment

   #  frappe.msgprint("<pre>{}</pre>".format(frappe.as_json(responses)))
   #  frappe.msgprint(responses)
    
    # Add answers
    parsed_data = json.loads(responses)
   #  frappe.msgprint("<pre>{}</pre>".format(parsed_data))
   #  frappe.msgprint("<pre>{}</pre>".format(parsed_data))
    for res in parsed_data:
      #   frappe.msgprint("<pre>{}</pre>".format(res)) # this works
      #   print("test")
      #   frappe.msgprint("<pre>{}</pre>".format(frappe.as_json(res)))
      #   option_doc = frappe.get_doc("Question Option", res['selected_option'])
        response.append("answers", {
            "question": res['question'],
            # "question": '2nd question - asm1-18-05-02',
            "selected_option": res['selected_option'],
            # "selected_option": 'op1-qn2-19-06',
            # "selected_option_text": option_doc.option_text,
            # "weight": option_doc.weight
        })
    
    # Insert and return response name
    response.insert(ignore_permissions=True)
    return response.name