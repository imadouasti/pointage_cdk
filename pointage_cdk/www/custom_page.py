import frappe

def get_context(context):
    context.about_us_settings = frappe.get_doc('About Us Settings')
    pointage_records_name = frappe.db.get_all("pointage", fields = ['name', 'employee','total_heure_supp'] )
    print("//////////////////////////////", pointage_records_name)
    return context

