import json
from typing import Any, Dict, List, Optional

import frappe
from frappe.utils import get_datetime
from frappe.model.document import Document


class BalanceSheet(Document):
	"""DocType Balance Sheet (parent).

	Lưu một lần submit của bảng cân đối kế toán (từ frontend), bao gồm raw JSON
	và bảng con Balance Sheet Item.
	"""

	pass


def _coerce_number(value: Any) -> float:
	"""Best-effort convert number-like to float."""
	if value is None or value == "":
		return 0.0
	try:
		return float(value)
	except Exception:
		return 0.0


def _validate_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
	if not isinstance(payload, dict):
		frappe.throw("Payload phải là JSON object")

	data = payload.get("data")
	if not isinstance(data, dict):
		frappe.throw("Thiếu trường data")

	# Chuẩn hóa report_type
	report_type = payload.get("report_type") or payload.get("reportType") or "income_statement"

	# Hỗ trợ 2 format:
	# - legacy: data = { assets: [], equity: [] }
	# - new:    data = { sections: { SectionName: [] } }
	sections = data.get("sections")
	if sections is not None:
		if not isinstance(sections, dict):
			frappe.throw("data.sections phải là object")
		normalized_sections: Dict[str, List[Dict[str, Any]]] = {}
		for k, v in sections.items():
			if v is None:
				v = []
			if not isinstance(v, list):
				frappe.throw(f"data.sections.{k} phải là array")
			normalized_sections[str(k)] = v
		return {
			"timestamp": payload.get("timestamp"),
			"report_type": report_type,
			"sections": normalized_sections,
		}

	# Legacy
	assets = data.get("assets") or []
	equity = data.get("equity") or []
	if not isinstance(assets, list) or not isinstance(equity, list):
		frappe.throw("assets/equity phải là array")

	return {
		"timestamp": payload.get("timestamp"),
		"report_type": report_type,
		"sections": {
			"Asset": assets,
			"Equity": equity,
		},
	}


@frappe.whitelist(allow_guest=False)
def save_balance_sheet(payload: Optional[Any] = None, name: Optional[str] = None):
	"""API nhận JSON từ frontend và lưu vào DocType.

	Endpoint:
		POST /api/method/custom_app.customdemo.doctype.balance_sheet.balance_sheet.save_balance_sheet

	Body (khuyến nghị):
		{ "payload": { ... } }
	Hoặc gửi trực tiếp JSON của payload (Frappe sẽ map args theo key).

	- Nếu truyền `name`: update document hiện có (replace toàn bộ items)
	- Nếu không: tạo mới
	"""
	# Frappe có thể truyền payload như string hoặc dict.
	if payload is None:
		# Khi frontend gửi trực tiếp {timestamp, data:{...}} thì payload None
		# và kwargs nằm trong frappe.local.form_dict
		payload_obj = dict(frappe.local.form_dict)
		# Loại bỏ các key phụ mà Frappe thêm
		payload_obj.pop("cmd", None)
		payload_obj.pop("csrf_token", None)
	else:
		payload_obj = frappe.parse_json(payload)

	normalized = _validate_payload(payload_obj)

	# raw json lưu nguyên bản để debug/trace
	raw_json_str = json.dumps(payload_obj, ensure_ascii=False)

	# Enforce one report per (report_type, fiscal_year).
	# - If `name` is provided: overwrite that document.
	# - If `name` is not provided: try to find existing doc by (report_type, fiscal_year) and overwrite it.
	if name:
		doc = frappe.get_doc("Balance Sheet", name)
		doc.items = []
	else:
		# upsert by filters (report_type + year)
		filters = {}
		filters["report_type"] = normalized.get("report_type") or payload_obj.get("report_type") or "tt200_income_statement"
		if payload_obj.get("fiscal_year"):
			filters["fiscal_year"] = payload_obj.get("fiscal_year")

		existing_name = None
		if filters:
			existing_name = frappe.db.get_value("Balance Sheet", filters, "name")

		if existing_name:
			doc = frappe.get_doc("Balance Sheet", existing_name)
			doc.items = []
			name = existing_name
		else:
			doc = frappe.new_doc("Balance Sheet")
			# title mặc định để dễ xem list
			doc.title = payload_obj.get("title") or f"Balance Sheet {frappe.utils.now()}"

	# set header fields
	doc.fiscal_year = payload_obj.get("fiscal_year")
	doc.currency = payload_obj.get("currency") or "VND"
	doc.report_type = normalized.get("report_type") or payload_obj.get("report_type") or "tt200_income_statement"

	# generated_at: accept ISO-8601 (vd: 2025-12-29T00:00:00Z)
	generated_at = normalized.get("timestamp")
	try:
		dt = get_datetime(generated_at) if generated_at else None
		# MariaDB DATETIME không nhận timezone offset -> convert về naive
		if dt and getattr(dt, 'tzinfo', None):
			dt = dt.astimezone(frappe.utils.timezone.utc).replace(tzinfo=None)
		elif dt:
			dt = dt.replace(tzinfo=None)
		doc.generated_at = dt
	except Exception:
		# nếu parse fail thì bỏ qua, không chặn lưu
		doc.generated_at = None
	doc.raw_json = raw_json_str

	def add_rows(rows: List[Dict[str, Any]], section: str):
		for r in rows:
			if not isinstance(r, dict):
				continue
			doc.append(
				"items",
				{
					"section": section,
					"source_id": r.get("id"),
					"source_parent_id": r.get("parentId"),
					"label": r.get("label"),
					"code": r.get("code"),
					"note": r.get("note"),
					"start_year": _coerce_number(r.get("startYear")),
					"end_year": _coerce_number(r.get("endYear")),
					"indent": int(r.get("indent") or 0),
				},
			)

	# sections: Dict[section_name -> rows]
	for section_name, rows in (normalized.get("sections") or {}).items():
		add_rows(rows, section_name)

	# Save/insert
	if name:
		doc.save()
	else:
		doc.insert()

	frappe.db.commit()
	return {"success": True, "name": doc.name}


@frappe.whitelist(allow_guest=False)
def delete_balance_sheet(name: Optional[str] = None, fiscal_year: Optional[str] = None, report_type: Optional[str] = None):
	"""Xóa Balance Sheet.

	Ưu tiên theo docname (name). Nếu không có name thì xóa theo (fiscal_year, circular_template).

	Trả về:
		{success: bool, deleted: int, message?: str}
	"""
	deleted = 0

	# 1) delete by explicit docname
	if name:
		try:
			doc = frappe.get_doc("Balance Sheet", name)
			doc.delete()
			frappe.db.commit()
			return {"success": True, "deleted": 1, "name": name}
		except frappe.DoesNotExistError:
			return {"success": True, "deleted": 0, "message": "Không tìm thấy bản ghi để xóa"}

	# 2) delete by filters
	filters = {}
	if report_type:
		filters["report_type"] = report_type
	if fiscal_year:
		filters["fiscal_year"] = fiscal_year

	if not filters:
		frappe.throw("Thiếu tham số: name hoặc fiscal_year/circular_template")

	# Xóa tất cả bản ghi khớp filters (phòng trường hợp trước đó có tạo nhiều bản)
	names = frappe.get_all("Balance Sheet", filters=filters, pluck="name")
	for n in names:
		frappe.delete_doc("Balance Sheet", n, ignore_permissions=False)
		deleted += 1

	frappe.db.commit()
	return {"success": True, "deleted": deleted}


@frappe.whitelist(allow_guest=False)
def get_report_types():
	"""Get list of active Report Types for dropdown"""
	report_types = frappe.get_all(
		"Report Type",
		filters={"is_active": 1},
		fields=["name", "code", "report_name", "circular_template", "sections_json"],
		order_by="circular_template, report_name"
	)
	return {"success": True, "data": report_types}


@frappe.whitelist(allow_guest=False)
def get_circular_templates():
	"""Get list of active Circular Templates for dropdown"""
	templates = frappe.get_all(
		"Circular Template",
		filters={"is_active": 1},
		fields=["name", "code", "template_name", "description"],
		order_by="template_name"
	)
	return {"success": True, "data": templates}


@frappe.whitelist(allow_guest=False)
def create_report_type(report_name: str, code: str, description: str = "", sections_json: str = "[]", is_active: int = 1):
	"""Create new Report Type"""
	if frappe.db.exists("Report Type", code):
		frappe.throw(f"Report Type with code '{code}' already exists")
	
	doc = frappe.get_doc({
		"doctype": "Report Type",
		"report_name": report_name,
		"code": code,
		"description": description,
		"sections_json": sections_json,
		"is_active": is_active
	})
	doc.insert()
	frappe.db.commit()
	return {"success": True, "message": "Created successfully", "name": doc.name}


@frappe.whitelist(allow_guest=False)
def update_report_type(name: str, report_name: str = None, description: str = None, sections_json: str = None, is_active: int = None):
	"""Update existing Report Type"""
	doc = frappe.get_doc("Report Type", name)
	if report_name:
		doc.report_name = report_name
	if description is not None:
		doc.description = description
	if sections_json is not None:
		doc.sections_json = sections_json
	if is_active is not None:
		doc.is_active = is_active
	doc.save()
	frappe.db.commit()
	return {"success": True, "message": "Updated successfully"}


@frappe.whitelist(allow_guest=False)
def delete_report_type(name: str):
	"""Delete Report Type"""
	frappe.delete_doc("Report Type", name)
	frappe.db.commit()
	return {"success": True, "message": "Deleted successfully"}


@frappe.whitelist(allow_guest=False)
def create_circular_template(template_name: str, code: str, description: str = "", is_active: int = 1):
	"""Create new Circular Template"""
	if frappe.db.exists("Circular Template", code):
		frappe.throw(f"Circular Template with code '{code}' already exists")
	
	doc = frappe.get_doc({
		"doctype": "Circular Template",
		"template_name": template_name,
		"code": code,
		"description": description,
		"is_active": is_active
	})
	doc.insert()
	frappe.db.commit()
	return {"success": True, "message": "Created successfully", "name": doc.name}


@frappe.whitelist(allow_guest=False)
def update_circular_template(name: str, template_name: str = None, description: str = None, is_active: int = None):
	"""Update existing Circular Template"""
	doc = frappe.get_doc("Circular Template", name)
	if template_name:
		doc.template_name = template_name
	if description is not None:
		doc.description = description
	if is_active is not None:
		doc.is_active = is_active
	doc.save()
	frappe.db.commit()
	return {"success": True, "message": "Updated successfully"}


@frappe.whitelist(allow_guest=False)
def delete_circular_template(name: str):
	"""Delete Circular Template"""
	frappe.delete_doc("Circular Template", name)
	frappe.db.commit()
	return {"success": True, "message": "Deleted successfully"}


@frappe.whitelist(allow_guest=False)
def get_balance_sheet(name: str, include_raw_json: int = 0):
	"""Lấy Balance Sheet theo docname.

	- Mặc định không trả raw_json để response gọn.
	"""
	doc = frappe.get_doc('Balance Sheet', name)
	data = doc.as_dict()
	if not int(include_raw_json):
		data.pop('raw_json', None)
	return data


@frappe.whitelist(allow_guest=False)
def get_balance_sheet_by_filters(fiscal_year: Optional[str] = None, report_type: Optional[str] = None):
	"""Tìm Balance Sheet theo năm tài chính và mẫu thông tư.
	
	Trả về Balance Sheet mới nhất khớp với filters.
	"""
	filters = {}
	if report_type:
		filters["report_type"] = report_type
	if fiscal_year:
		filters["fiscal_year"] = fiscal_year

	# Tìm doc mới nhất
	docs = frappe.get_all(
		"Balance Sheet",
		filters=filters,
		fields=["name", "title", "fiscal_year", "currency", "report_type", "generated_at"],
		order_by="generated_at desc",
		limit=1
	)







	
	if not docs:
		return {"success": False, "message": "Không tìm thấy báo cáo phù hợp"}
	
	# Lấy full doc với items
	doc = frappe.get_doc("Balance Sheet", docs[0].name)
	data = doc.as_dict()
	
	# Parse raw_json để trả về dạng frontend cần
	try:
		if data.get("raw_json"):
			parsed = json.loads(data["raw_json"])
			parsed_data = parsed.get("data", {})
			# Normalize return format to always provide data.sections
			if isinstance(parsed_data, dict) and isinstance(parsed_data.get("sections"), dict):
				data["parsed_data"] = {"sections": parsed_data.get("sections")}
			else:
				# legacy payload (assets/equity)
				data["parsed_data"] = {
					"sections": {
						"Asset": (parsed_data.get("assets") if isinstance(parsed_data, dict) else []) or [],
						"Equity": (parsed_data.get("equity") if isinstance(parsed_data, dict) else []) or [],
					}
				}
	except Exception:
		pass
	
	data.pop("raw_json", None)
	return {"success": True, "data": data}
