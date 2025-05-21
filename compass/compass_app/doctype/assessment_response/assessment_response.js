// Copyright (c) 2025, JinsoRaj and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Assessment Response", {
// 	refresh(frm) {

// 	},
// });


console.log("Assessment Response JS loaded");

// assessment_response.js
frappe.ui.form.on('Assessment Response', {
   refresh(frm) {
       initialize_filters(frm);
   },
   answers_add(frm, cdt, cdn) {
       setup_option_filter(frm, cdn);
   }
});

frappe.ui.form.on('Assessment Answer', {
   question(frm, cdt, cdn) {
       setup_option_filter(frm, cdn);
   }
});

function initialize_filters(frm) {
   if (!frm.fields_dict.answers?.grid) {
       setTimeout(() => initialize_filters(frm), 500);
       return;
   }
   frm.fields_dict.answers.grid.grid_rows.forEach(row => {
       setup_option_filter(frm, row.doc.name);
   });
}

function setup_option_filter(frm, row_name) {
   const row = frappe.model.get_doc('Assessment Answer', row_name);
   const df = frappe.meta.get_docfield('Assessment Answer', 'selected_option', row_name);
   
   df.get_query = () => ({
       filters: { parent: row.question },
       strict: true
   });
   
   refresh_field('selected_option', row_name, 'answers');
}