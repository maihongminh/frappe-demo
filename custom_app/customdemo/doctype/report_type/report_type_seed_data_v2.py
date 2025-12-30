# Script to create seed data for Report Type (with Circular Template link)
import frappe

def recreate_report_types():
	"""Delete old Report Types and create new ones with Circular Template"""
	
	# Delete existing Report Types
	existing = frappe.get_all("Report Type", pluck="name")
	for name in existing:
		frappe.delete_doc("Report Type", name, force=1, ignore_permissions=True)
	
	frappe.db.commit()
	print(f"Deleted {len(existing)} existing Report Types")
	
	# New Report Types with Circular Template
	report_types = [
		# Thông tư 200
		{
			"code": "tt200_income_statement",
			"report_name": "Báo cáo tình hình kinh doanh (TT200)",
			"circular_template": "200",
			"description": "Income Statement - Circular 200/2014/TT-BTC",
			"sections_json": '["Revenue", "Expense", "Other"]',
			"is_active": 1
		},
		{
			"code": "tt200_cash_flow",
			"report_name": "Báo cáo lưu chuyển tiền tệ (TT200)",
			"circular_template": "200",
			"description": "Cash Flow Statement - Circular 200/2014/TT-BTC",
			"sections_json": '["Operating", "Investing", "Financing"]',
			"is_active": 1
		},
		{
			"code": "tt200_balance_sheet",
			"report_name": "Bảng cân đối kế toán (TT200)",
			"circular_template": "200",
			"description": "Balance Sheet - Circular 200/2014/TT-BTC",
			"sections_json": '["Asset", "Equity"]',
			"is_active": 1
		},
		
		# Thông tư 133
		{
			"code": "tt133_income_statement",
			"report_name": "Báo cáo tình hình kinh doanh (TT133)",
			"circular_template": "133",
			"description": "Income Statement - Circular 133/2016/TT-BTC",
			"sections_json": '["Revenue", "Expense", "Other"]',
			"is_active": 1
		},
		{
			"code": "tt133_cash_flow",
			"report_name": "Báo cáo lưu chuyển tiền tệ (TT133)",
			"circular_template": "133",
			"description": "Cash Flow Statement - Circular 133/2016/TT-BTC",
			"sections_json": '["Operating", "Investing", "Financing"]',
			"is_active": 1
		},
		{
			"code": "tt133_balance_sheet",
			"report_name": "Bảng cân đối kế toán (TT133)",
			"circular_template": "133",
			"description": "Balance Sheet - Circular 133/2016/TT-BTC",
			"sections_json": '["Asset", "Equity"]',
			"is_active": 1
		},
	]
	
	for rt in report_types:
		doc = frappe.get_doc({
			"doctype": "Report Type",
			**rt
		})
		doc.insert(ignore_permissions=True)
		print(f"Created Report Type: {rt['report_name']}")
	
	frappe.db.commit()
	print(f"\nTotal created: {len(report_types)} Report Types")

if __name__ == "__main__":
	recreate_report_types()
