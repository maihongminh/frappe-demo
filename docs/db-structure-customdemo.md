# Cấu trúc DB (custom_app/customdemo)

Tài liệu này mô tả các bảng DB được sinh từ các DocType trong module `customdemo` của app `custom_app` (bench: `frappe-test`).

**Quy ước:**
- Mỗi DocType tương ứng 1 bảng MariaDB/MySQL tên `tab<DocType Name>`.
- Chỉ liệt kê các field custom định nghĩa trong DocType JSON. **Các field hệ thống** (vd: `name`, `owner`, `creation`, `modified`, `docstatus`, …) không hiển thị theo yêu cầu.
- Các field dạng layout (Section Break/Column Break/…) không tạo cột DB nên cũng không liệt kê.

## Balance Sheet

- **Bảng DB:** `tabBalance Sheet`
- **Module:** `customdemo`
- **Loại:** Master/Transaction

### Các field custom

| fieldname | label | type | ràng buộc | ghi chú |
|---|---|---|---|---|
| `title` | Title | `Data` | required, in_list_view |  |
| `fiscal_year` | Năm tài chính | `Data` | in_list_view |  |
| `currency` | Loại tiền tệ | `Data` | default=VND |  |
| `report_type` | Loại báo cáo | `Link` | required, in_list_view | Link tới `Report Type` |
| `report_date` | Report Date | `Date` | in_list_view |  |
| `generated_at` | Generated At | `Datetime` |  |  |
| `raw_json` | Raw JSON | `Long Text` |  | text field |
| `items` | Items | `Table` |  | Child table: `Balance Sheet Item` (lưu dòng con ở `tabBalance Sheet Item`) |

### Ghi chú

**Mục đích sử dụng:** Lưu dữ liệu báo cáo tài chính theo **năm tài chính** và **loại báo cáo** (Report Type). Frontend màn `BalanceSheet.vue` cho phép chọn thông tư (Circular Template) → loại báo cáo (Report Type) → năm tài chính, sau đó nhập số liệu và lưu.

**Quan hệ:**
- `report_type` là **Link** tới `Report Type` (mỗi Balance Sheet thuộc 1 loại báo cáo).
- `items` là **Child Table** (`Balance Sheet Item`) chứa các dòng chỉ tiêu của báo cáo.

**Luồng API (backend: `custom_app.customdemo.doctype.balance_sheet.balance_sheet`):**
- `save_balance_sheet(payload, name=None)` (POST)
  - Nếu có `name` → **update** doc đó và **replace toàn bộ** `items`.
  - Nếu không có `name` → backend cố gắng **upsert** theo bộ lọc `(report_type, fiscal_year)`:
    - tìm existing doc bằng `frappe.db.get_value('Balance Sheet', filters, 'name')`
    - nếu có → update + replace items
    - nếu không → insert doc mới
- `get_balance_sheet_by_filters(fiscal_year, report_type)` (GET)
  - Trả về bản ghi mới nhất theo `generated_at desc`, kèm `parsed_data.sections` để frontend dựng lại bảng.
- `delete_balance_sheet(name=None, fiscal_year=None, report_type=None)` (POST)
  - Ưu tiên xoá theo `name` (docname), nếu không có thì xoá theo filter.

**Mapping dữ liệu frontend → DB:**
- Frontend lưu theo JSON dạng:
  - `payload.title` → `Balance Sheet.title`
  - `payload.fiscal_year` → `Balance Sheet.fiscal_year`
  - `payload.currency` → `Balance Sheet.currency`
  - `payload.report_type` → `Balance Sheet.report_type`
  - `payload.timestamp` → `Balance Sheet.generated_at` (backend parse ISO-8601 và bỏ timezone nếu có)
  - `payload` nguyên bản được dump vào `Balance Sheet.raw_json` để trace/debug
- `payload.data.sections` (object) được backend normalize và map thành các dòng `Balance Sheet Item`:
  - `row.id` → `items.source_id`
  - `row.parentId` → `items.source_parent_id`
  - `row.label` → `items.label`
  - `row.code` → `items.code`
  - `row.note` → `items.note`
  - `row.startYear` → `items.start_year` (coerce sang float)
  - `row.endYear` → `items.end_year` (coerce sang float)
  - `row.indent` → `items.indent` (int)
  - Tên section (vd `Asset`, `Equity`, …) → `items.section`

**Lưu ý dữ liệu:** Backend hỗ trợ 2 format payload:
- Mới: `data.sections` là object (map section → array)
- Legacy: `data.assets` và `data.equity` (backend tự normalize về `sections.Asset`/`sections.Equity`)



## Balance Sheet Item

- **Bảng DB:** `tabBalance Sheet Item`
- **Module:** `customdemo`
- **Loại:** Child Table (`istable=1`)

### Các field custom

| fieldname | label | type | ràng buộc | ghi chú |
|---|---|---|---|---|
| `section` | Section | `Select` | required, in_list_view | options: Asset, Equity, Revenue, Expense, Other, Operating, Investing, Financing |
| `source_id` | Source ID | `Data` | in_list_view |  |
| `source_parent_id` | Source Parent ID | `Data` |  |  |
| `label` | Label | `Data` | required, in_list_view |  |
| `code` | Code | `Data` |  |  |
| `note` | Note | `Data` |  |  |
| `start_year` | Start Year | `Float` |  |  |
| `end_year` | End Year | `Float` |  |  |
| `indent` | Indent | `Int` |  |  |

> Ghi chú (Child Table): Frappe tự tạo các cột quan hệ để gắn dòng con vào parent: `parent`, `parenttype`, `parentfield` và `idx` (không liệt kê chi tiết ở đây vì là field hệ thống).

### Ghi chú

**Vai trò:** Là dòng chi tiết (child row) của `Balance Sheet`.

**Ý nghĩa các field:**
- `section`: nhóm chỉ tiêu (Asset/Equity/Revenue/Expense/Other/Operating/Investing/Financing). Phía UI dùng để group theo section.
- `source_id` và `source_parent_id`: lưu id dạng string từ template/GUI để thể hiện cấu trúc cây (cha–con).
- `indent`: mức thụt lề (0/1/2…) phục vụ hiển thị dạng cây ở frontend.
- `start_year`, `end_year`: số liệu đầu năm/cuối năm.

**Nguồn dữ liệu:** Được sinh khi gọi `save_balance_sheet` (backend append vào `doc.items`). Không thấy API CRUD riêng cho từng item; items được quản lý theo kiểu replace toàn bộ theo parent.



## Balance Sheet Report

- **Bảng DB:** `tabBalance Sheet Report`
- **Module:** `customdemo`
- **Loại:** Master/Transaction

### Các field custom

| fieldname | label | type | ràng buộc | ghi chú |
|---|---|---|---|---|
| `report_name` | Report Name | `Data` | required, in_list_view |  |
| `generated_at` | Generated At | `Datetime` |  |  |
| `raw_json` | Raw JSON | `Long Text` |  | text field |

### Ghi chú

Hiện tại trong codebase chưa thấy frontend/back-end sử dụng DocType này trong luồng chính (BalanceSheet.vue đang làm việc trực tiếp với `Balance Sheet` + `Balance Sheet Item`).

DocType này có thể dùng để lưu snapshot báo cáo dạng JSON theo tên report, nhưng cần kiểm tra/định nghĩa thêm luồng ghi dữ liệu nếu muốn dùng thực tế.



## Circular Template

- **Bảng DB:** `tabCircular Template`
- **Module:** `customdemo`
- **Loại:** Master/Transaction
- **Naming (autoname):** `field:code`

### Các field custom

| fieldname | label | type | ràng buộc | ghi chú |
|---|---|---|---|---|
| `template_name` | Template Name | `Data` | required, in_list_view |  |
| `code` | Code | `Data` | required, unique, in_list_view |  |
| `description` | Description | `Small Text` |  | text field |
| `is_active` | Is Active | `Check` | in_list_view, default=1 |  |

### Ghi chú

**Mục đích:** Danh mục “thông tư/mẫu” để nhóm các `Report Type`.

**Luồng API liên quan (nằm trong `balance_sheet.py`):**
- `get_circular_templates()` (GET): trả các template active.
- `create_circular_template(...)`, `update_circular_template(...)`, `delete_circular_template(name)`.

**Seed data:**
- `circular_template_seed_data.py` tạo sẵn các bản ghi: `200` (TT200), `133` (TT133), `other`.

**Ràng buộc:**
- DocType đặt `autoname = field:code` và field `code` là `unique`.



## Customer

- **Bảng DB:** `tabCustomer`
- **Module:** `customdemo`
- **Loại:** Master/Transaction

### Các field custom

| fieldname | label | type | ràng buộc | ghi chú |
|---|---|---|---|---|
| `customer_name` | Customer Name | `Data` | required, in_list_view |  |
| `email` | Email | `Data` |  |  |
| `phone` | Phone | `Data` |  |  |
| `role` | Role | `Select` |  | options: Customer, VIP, Partner |
| `address` | Address | `Small Text` |  | text field |

### Ghi chú

**Mục đích sử dụng:** Demo quản lý khách hàng trên UI (CustomerList/CustomerEdit).

**Ràng buộc nghiệp vụ (backend validate):**
- Trong `Customer.validate()`:
  - Bắt buộc phải có **Email hoặc Phone** (không được bỏ trống cả hai).
  - Nếu có email thì phải chứa ký tự `@`.

**Luồng API (backend: `custom_app.customdemo.doctype.customer.customer`):**
- `get_customers()` (POST): lấy danh sách tối đa 50 bản ghi gần nhất (`order_by='modified desc'`), trả về các field: `name`, `customer_name`, `email`, `phone`, `role`, `address`.
- `create_customer(customer_name, email, phone, role, address)` (POST): tạo mới.
- `get_customer(name)` (POST): lấy chi tiết theo docname.
- `update_customer(name, ...)` (POST): cập nhật theo docname.
- `delete_customer(name)` (POST): xoá theo docname.

**Ghi chú UI:**
- Form tạo mới yêu cầu `customer_name` (required ở frontend + DocType).
- UI filter/search client-side theo `customer_name/email/phone/address` và lọc theo `role`.



## Report Type

- **Bảng DB:** `tabReport Type`
- **Module:** `customdemo`
- **Loại:** Master/Transaction
- **Naming (autoname):** `field:code`

### Các field custom

| fieldname | label | type | ràng buộc | ghi chú |
|---|---|---|---|---|
| `report_name` | Report Name | `Data` | required, in_list_view |  |
| `code` | Code | `Data` | required, unique, in_list_view |  |
| `circular_template` | Circular Template | `Link` | required, in_list_view | Link tới `Circular Template` |
| `description` | Description | `Text` |  | text field |
| `sections_json` | Sections Configuration (JSON) | `Long Text` |  | text field |
| `is_active` | Is Active | `Check` | in_list_view, default=1 |  |

### Ghi chú

**Mục đích:** Định nghĩa **loại báo cáo** (ví dụ: Balance Sheet, Income Statement, Cash Flow...) và cấu hình **danh sách sections** cần hiển thị.

**Quan hệ:**
- `circular_template` (Link → `Circular Template`): nhóm Report Type theo thông tư (TT200/TT133/...).
- `sections_json`: JSON array dạng string, ví dụ `["Asset", "Equity"]`.
  - Frontend parse trường này để quyết định render các section nào.

**Luồng API liên quan (nằm trong `balance_sheet.py`):**
- `get_report_types()` (GET): trả các Report Type active (`is_active=1`) gồm `name`, `code`, `report_name`, `circular_template`, `sections_json`.
- `create_report_type(...)`, `update_report_type(...)`, `delete_report_type(name)`.

**Seed data:**
- Có script seed `report_type_seed_data_v2.py` tạo các Report Type cho TT200/TT133 với `sections_json` tương ứng.

**Ràng buộc:**
- DocType đặt `autoname = field:code` và field `code` là `unique` → về logic, `code` đóng vai trò “mã định danh” ổn định.
