# Tạo 1 trang index thủ công cho site

Tạo 1 file index dùng để thay thế trang ban đầu (view website) trong đường dẫn:

```
/frappe-demo/apps/custom_app/custom_app/templates/pages
```

## Ví dụ: Cấu trúc cơ bản của 1 file index

```jinja
{% extends "templates/web.html" %}
{% block title %}{{ _("Home") }}{% endblock %}
{% block page_content %}
    {# Viết giao diện chính của trang index vào đây #}
{% endblock %}
```

**Giải thích:**

- `{% extends "templates/web.html" %}`: Kế thừa (extend) từ template gốc `web.html`, chứa cấu trúc HTML chuẩn (header, navbar, footer, meta tags, CSS/JS chung...)
- `{% block title %}`: Set title cho tab trình duyệt
- `{% block page_content %}`: Viết giao diện chính của trang index vào đây

> **Lưu ý:** Phần `extends` có thể bỏ qua và thay thế bằng giao diện tự custom.

---

# Tạo 1 DocType cơ bản bằng code

## Tạo thư mục chứa DocType

Ví dụ: `custom_app/custom_app/customdemo/doctype/customer/`

## Cấu trúc cần có để khởi tạo 1 DocType

```
custom_app/
└── custom_app/
    └── customdemo/
        └── doctype/
            └── customer/
                ├── __init__.py         # python package marker
                ├── customer.json       # định nghĩa DocType
                ├── customer.py         # controller (viết logic backend: API, validate)
                ├── customer.js         # js (viết logic frontend)
                └── test_customer.py    # unit tests
```

---

## customer.js

```javascript
frappe.ui.form.on('Customer', {
    // Hook chạy khi form load/reload
    refresh: function(frm) {
    },
    
    validate: function(frm) {
        // kiểm tra mail, phone
        if (!frm.doc.email && !frm.doc.phone) {
            frappe.throw('Vui lòng nhập Email hoặc Phone');
        }
        
        // email format
        if (frm.doc.email && !frm.doc.email.includes('@')) {
            frappe.throw('Email không hợp lệ');
        }
    },
});
```

**Giải thích:**

- `frappe.ui.form.on()`: Hàm của Frappe để đăng ký event handler cho form
- `'Customer'`: Tên DocType phải khớp với tên trong `customer.json`

---

## customer.json (demo cấu trúc cơ bản)

```json
{
  "actions": [],
  "allow_rename": 1,
  "creation": "2025-12-17 13:30:00.000000",
  "doctype": "DocType",
  "editable_grid": 1,
  "engine": "InnoDB",
  "field_order": [
    "customer_name",
    "email",
    "phone",
    "role",
    "address"
  ],
  "fields": [
    {
      "fieldname": "customer_name",
      "fieldtype": "Data",
      "in_list_view": 1,
      "label": "Customer Name",
      "reqd": 1
    },
    {
      "fieldname": "email",
      "fieldtype": "Data",
      "label": "Email",
      "options": "Email"
    },
    {
      "fieldname": "phone",
      "fieldtype": "Data",
      "label": "Phone"
    },
    {
      "fieldname": "role",
      "fieldtype": "Select",
      "label": "Role",
      "options": "Customer\nVIP\nPartner"
    },
    {
      "fieldname": "address",
      "fieldtype": "Small Text",
      "label": "Address"
    }
  ],
  "index_web_pages_for_search": 0,
  "links": [],
  "modified": "2025-12-17 13:30:00.000000",
  "modified_by": "Administrator",
  "module": "customdemo",
  "name": "Customer",
  "owner": "Administrator",
  "permissions": [
    {
      "create": 1,
      "delete": 1,
      "email": 1,
      "export": 1,
      "print": 1,
      "read": 1,
      "report": 1,
      "role": "System Manager",
      "share": 1,
      "write": 1
    }
  ],
  "sort_field": "modified",
  "sort_order": "DESC",
  "states": [],
  "track_changes": 1
}
```

**Giải thích - Những dòng cần lưu ý:**

- `"doctype": "DocType"`: Đây là dòng định nghĩa DocType
- `"name": "Customer"`: Tên DocType
- `"module": "customdemo"`: Module chứa DocType
- `"fields"`: Các trường trong database
- `"permissions"`: Phân quyền
  - Role "System Manager" có đầy đủ quyền thêm, sửa, xóa...
  - `1` (cho phép), `0` (chặn)

---

## customer.py (demo cơ bản)

```python
import frappe
from frappe.model.document import Document

# Import module của Frappe, cung cấp các hàm và class như:
# frappe.get_all(), frappe.get_doc(), frappe.throw(), frappe.db.commit(),
# frappe.whitelist(), frappe.call()

class Customer(Document):
    # Kế thừa từ Document, Frappe sẽ tự động map class này với DocType "Customer" từ customer.json
    
    def validate(self):
        """Chạy tự động trước khi save (cả Desk UI và API)"""
        # kiểm tra mail, phone
        if not self.email and not self.phone:
            frappe.throw("Vui lòng nhập Email hoặc Phone")
        
        # format email
        if self.email and '@' not in self.email:
            frappe.throw("Email không hợp lệ")
    
    def before_save(self):
        """Chạy trước khi save"""
        pass
    
    def after_insert(self):
        """Chạy sau khi insert thành công"""
        pass

@frappe.whitelist(allow_guest=False)
# Cho phép gọi từ JavaScript/REST API, yêu cầu đăng nhập (không cho guest)
def get_customers():
    """Get list customers"""
    return frappe.get_all(
        "Customer",
        fields=["name", "customer_name", "email", "phone", "role", "address"],
        order_by="modified desc",
        limit=50,
    )

@frappe.whitelist(allow_guest=False)
def create_customer(customer_name, email=None, phone=None, role=None, address=None):
    """Create a new customer"""
    doc = frappe.get_doc({
        "doctype": "Customer",
        "customer_name": customer_name,
        "email": email,
        "phone": phone,
        "role": role,
        "address": address,
    })
    doc.insert()  # Dòng này insert vào db (MariaDB)
    frappe.db.commit()  # Commit transaction vào db (Trong hàm API phải commit thủ công, không tự động như dùng UI của Frappe)
    return {"success": True, "name": doc.name}
```

---

## test_customer.py

```python
import frappe
from frappe.tests.utils import FrappeTestCase

class TestCustomer(FrappeTestCase):
    pass
```

> **Lưu ý:** File này là template dùng để tạo các test case.

---

## Migrate DocType

Sau khi tạo/chỉnh sửa DocType, nhớ chạy lại migrate để thêm DocType và tạo ra bảng mới trong database:

```bash
cd /home/minhmh/frappe-demo
bench --site customdemo.test migrate
```
