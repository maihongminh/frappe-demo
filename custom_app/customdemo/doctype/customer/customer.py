import frappe
from frappe.model.document import Document


class Customer(Document):
	"""
	DocType Customer - class đại diện cho từng bản ghi Customer.
	Các hook validate/before_save/after_insert sẽ chạy tự động khi thao tác với document.
	"""

	def validate(self):
		"""
		Hook validate
		- Chạy tự động khi save (cả từ Desk UI và khi gọi API)
		- Dùng để kiểm tra dữ liệu trước khi lưu vào database
		"""
		# kiểm tra mail,phone
		if not self.email and not self.phone:
			frappe.throw("Vui lòng nhập Email hoặc Phone")
		
		# kiểm tra format email
		if self.email and '@' not in self.email:
			frappe.throw("Email không hợp lệ")
	
	def before_save(self):
		"""
		Hook before_save
		- Chạy trước khi document được lưu
		- Có thể dùng để chuẩn hóa dữ liệu, set default,...
		"""
		pass
	
	def after_insert(self):
		"""
		Hook after_insert
		- Chạy sau khi insert thành công bản ghi mới
		- Có thể dùng để log, gửi email, tạo bản ghi liên quan,...
		"""
		pass


@frappe.whitelist(allow_guest=False)
def get_customers():
	"""
	 danh sách Customer mới nhất
	"""
	return frappe.get_all(
		"Customer",
		fields=["name", "customer_name", "email", "phone", "role", "address"],
		order_by="modified desc",
		limit=50,
	)


@frappe.whitelist(allow_guest=False)
def create_customer(customer_name, email=None, phone=None, role=None, address=None):
	"""
	thêm mới Customer
	"""
	doc = frappe.get_doc({
		"doctype": "Customer",
		"customer_name": customer_name,
		"email": email,
		"phone": phone,
		"role": role,
		"address": address,
	})
	doc.insert()
	frappe.db.commit()
	return {"success": True, "name": doc.name}


@frappe.whitelist(allow_guest=False)

def delete_customer(name: str):
	"""
	Xóa  Customer theo docname
	"""
	# name: docname của Customer lấy từ trường "name" trong list/get_customers
	frappe.delete_doc("Customer", name, ignore_permissions=False)
	frappe.db.commit()
	return {"success": True, "name": name}


@frappe.whitelist(allow_guest=False)
def get_customer(name: str):
	"""chi tiết của Customer
	dùng để load lại đata khi chỉnh sửa
	"""
	doc = frappe.get_doc("Customer", name)
	return doc.as_dict()


@frappe.whitelist(allow_guest=False)
def update_customer(name: str, customer_name=None, email=None, phone=None, role=None, address=None):
	"""
	sự kiện update
	"""
	doc = frappe.get_doc("Customer", name)

	# Chỉ update khi có chỉnh sửa giá trị
	if customer_name is not None:
		doc.customer_name = customer_name
	if email is not None:
		doc.email = email
	if phone is not None:
		doc.phone = phone
	if role is not None:
		doc.role = role
	if address is not None:
		doc.address = address

	# save() sẽ tự gọi validate()  trước khi ghi vào db
	doc.save()
	frappe.db.commit()

	return {"success": True, "name": doc.name}
