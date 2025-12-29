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

	# Frontend hiện tại gửi: { timestamp, data: { assets: [], equity: [] } }
	data = payload.get("data")
	if not isinstance(data, dict):
		frappe.throw("Thiếu trường data")

	assets = data.get("assets") or []
	equity = data.get("equity") or []
	if not isinstance(assets, list) or not isinstance(equity, list):
		frappe.throw("assets/equity phải là array")

	return {
		"timestamp": payload.get("timestamp"),
		"assets": assets,
		"equity": equity,
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

	if name:
		doc = frappe.get_doc("Balance Sheet", name)
		doc.items = []
	else:
		doc = frappe.new_doc("Balance Sheet")
		# title mặc định để dễ xem list
		doc.title = payload_obj.get("title") or f"Balance Sheet {frappe.utils.now()}"

	# set header fields
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

	add_rows(normalized["assets"], "Asset")
	add_rows(normalized["equity"], "Equity")

	# Save/insert
	if name:
		doc.save()
	else:
		doc.insert()

	frappe.db.commit()
	return {"success": True, "name": doc.name}


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
