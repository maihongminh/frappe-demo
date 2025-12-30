# Script to create seed data for Report Type
import frappe

def create_report_types():
	"""Create default Report Type records"""
	report_types = [
		{
			"code": "income_statement",
			"report_name": "Báo cáo tình hình kinh doanh",
			"description": "Income Statement / Profit & Loss Statement",
			"sections_json": '["Revenue", "Expense", "Other"]',
			"is_active": 1
		},
		{
			"code": "cash_flow_statement",
			"report_name": "Báo cáo lưu chuyển tiền tệ",
			"description": "Cash Flow Statement",
			"sections_json": '["Operating", "Investing", "Financing"]',
			"is_active": 1
		},
		{
			"code": "balance_sheet",
			"report_name": "Bảng cân đối kế toán",
			"description": "Balance Sheet / Statement of Financial Position",
			"sections_json": '["Asset", "Equity"]',
			"is_active": 1
		}
	]
	
	for rt in report_types:
		if not frappe.db.exists("Report Type", rt["code"]):
			doc = frappe.get_doc({
				"doctype": "Report Type",
				**rt
			})
			doc.insert(ignore_permissions=True)
			print(f"Created Report Type: {rt['report_name']}")
		else:
			print(f"Report Type already exists: {rt['code']}")
	
	frappe.db.commit()

if __name__ == "__main__":
	create_report_types()
