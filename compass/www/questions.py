import frappe

def get_context(context):
    # Get assessment name from route
   assessment_name = frappe.form_dict.get("assessment")
   if not assessment_name:
      frappe.throw("Invalid assessment URL", frappe.PermissionError)

   # Fetch assessment with questions and options
   assessment = frappe.get_doc("Assessment", assessment_name)
   # Prepare questions with options
   questions = []
   for q in assessment.questions:
      question_doc = frappe.get_doc("Question", q.question)
      options = sorted(question_doc.options, key=lambda x: x.rank)
      questions.append({
         "name": question_doc.name,
         "text": question_doc.question_text,
         "options": options
      })

   context.assessment = {
      "name": assessment.name,
      "title": assessment.assessment_name,
      "questions": questions
   }

   return context
