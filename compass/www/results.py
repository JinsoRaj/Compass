import frappe

def get_context(context):
      
   # Get response name from route
   response_name = frappe.form_dict.get("response")
   if not response_name:
      frappe.throw("Invalid response URL", frappe.PermissionError)

   # Fetch response document
   context.response = frappe.get_doc("Assessment Response", response_name)
   context.assessment = frappe.get_doc("Assessment", context.response.assessment)



   # Fetch all relevant pillars
   context.pillars = frappe.get_all(
      "Pillar",
      filters={"assessment_name": context.response.assessment},
      fields=["pillar_name", "pillar_description"]
   )

   # Create a lookup dictionary for pillar descriptions
   pillar_desc_map = {p["pillar_name"]: p["pillar_description"] for p in context.pillars}

   # Assign descriptions using dictionary's get method (returns None if not found)
   context.pillar_1_desc = pillar_desc_map.get(context.response.pillar_1_text)
   context.pillar_2_desc = pillar_desc_map.get(context.response.pillar_2_text)
   context.pillar_3_desc = pillar_desc_map.get(context.response.pillar_3_text)

   return context
