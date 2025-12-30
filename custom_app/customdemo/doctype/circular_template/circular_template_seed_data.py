# Script to create seed data for Circular Template
import frappe

def create_circular_templates():
	"""Create default Circular Template records"""
	templates = [
		{
			"code": "200",
			"template_name": "Thông tư 200",
			"description": "Thông tư 200/2014/TT-BTC",
			"is_active": 1
		},
		{
			"code": "133",
			"template_name": "Thông tư 133",
			"description": "Thông tư 133/2016/TT-BTC",
			"is_active": 1
		},
		{
			"code": "other",
			"template_name": "Khác",
			"description": "Mẫu tự do khác",
			"is_active": 1
		}
	]
	
	for tmpl in templates:
		if not frappe.db.exists("Circular Template", tmpl["code"]):
			doc = frappe.get_doc({
				"doctype": "Circular Template",
				**tmpl
			})
			doc.insert(ignore_permissions=True)
			print(f"Created Circular Template: {tmpl['template_name']}")
		else:
			print(f"Circular Template already exists: {tmpl['code']}")
	
	frappe.db.commit()

if __name__ == "__main__":
	create_circular_templates()
