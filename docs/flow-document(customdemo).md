# Custom App - Tài Liệu flow Hoạt Động

## Mục Lục

1. [Tổng Quan](#tổng-quan)
2. [Kiến Trúc Hệ Thống](#kiến-trúc-hệ-thống)
3. [Flow Khởi Động](#Flow-khởi-động)
4. [Flow Tạo Mới Customer](#Flow-tạo-mới-customer)
5. [Flow Xem Danh Sách Customer](#Flow-xem-danh-sách-customer)
6. [Flow Chỉnh Sửa Customer](#Flow-chỉnh-sửa-customer)
7. [Flow Xóa Customer](#Flow-xóa-customer)
8. [Flow Filter và Search](#Flow-filter-và-search)
9. [Backend API Flow](#backend-api-flow)
10. [Frontend Component Flow](#frontend-component-flow)

---

## Tổng Quan

**Custom App** là ứng dụng quản lý Customer được xây dựng trên:
- **Backend**: Frappe Framework (Python) - Xử lý business logic và database
- **Frontend**: Vue.js 3 - Giao diện người dùng
- **Database**: MySQL/MariaDB thông qua Frappe ORM

### Các Chức Năng Chính

1.  Tạo mới Customer
2.  Xem danh sách Customer
3.  Chỉnh sửa Customer
4.  Xóa Customer
5.  Tìm kiếm và lọc Customer

---

## Kiến Trúc Hệ Thống

### Cấu Trúc Thư Mục

```
custom_app/
├── custom_app/
│   ├── hooks.py                    # Cấu hình Frappe hooks
│   ├── customdemo/
│   │   └── doctype/
│   │       └── customer/
│   │           ├── customer.py     # Backend API & Document class
│   │           └── customer.json  # DocType definition
│   ├── frontend/
│   │   └── src/
│   │       ├── main.js            # Vue app entry point
│   │       ├── App.vue            # Root component (Router)
│   │       └── components/
│   │           ├── CustomerList.vue
│   │           └── CustomerEdit.vue
│   ├── public/
│   │   └── frontend/js/main.js    # Compiled Vue app
│   ├── templates/pages/
│   │   └── index.html             # Home page template
│   └── www/
│       ├── vue_demo.html          # Vue app page
│       ├── feature1.html          # Customer list page
│       └── feature1_edit.html    # Customer edit page
```



## Flow Khởi Động

### Bước 1: User Truy Cập Trang

**URL:** `http://site:8000/` hoặc `http://site:8000/vue_demo`

**File liên quan:** `templates/pages/index.html` hoặc `www/vue_demo.html`

```html
{% extends "templates/web.html" %}
{% block page_content %}
<div id="vue-app"></div>
{% endblock %}
{% block script %}
<script src="/assets/custom_app/frontend/js/main.js"></script>
{% endblock %}
```

**Flow:**
1. Browser request → Frappe server
2. Frappe load template `index.html` hoặc `vue_demo.html`
3. Template render HTML với `<div id="vue-app"></div>`
4. Load script `/assets/custom_app/frontend/js/main.js`

---

### Bước 2: Vue App Mount

**File:** `frontend/src/main.js`

```javascript
import { createApp } from 'vue';
import App from './App.vue';

const app = createApp(App);

// Mount khi frappe.ready
frappe.ready(() => {
  app.mount('#vue-app');
});
```

**Flow:**
1. Script `main.js` được load
2. Import Vue và App component
3. Tạo Vue app instance
4. Chờ `frappe.ready()` callback
5. Mount app vào element `#vue-app`

**Timeline:**
```
DOM Load → Script Load → frappe.ready() → Vue Mount
```

---

### Bước 3: App.vue Khởi Tạo

**File:** `frontend/src/App.vue`

```javascript
mounted() {
  this.initializeView();  // Chạy khi component mount
}

initializeView() {
  const path = window.location.pathname;
  
  if (path.startsWith('/feature1_edit')) {
    this.currentView = 'customer_edit';
    this.editCustomerName = getQueryParam('name');
  } else if (path.startsWith('/feature1')) {
    this.currentView = 'customer_list';
  } else {
    this.currentView = 'home';  // Default
  }
}
```

**Flow:**
1. `App.vue` component mount
2. Gọi `initializeView()` để xác định view hiện tại
3. Kiểm tra URL path:
   - `/feature1_edit?name=...` → `customer_edit`
   - `/feature1` → `customer_list`
   - `/` hoặc `/vue_demo` → `home`
4. Set `currentView` tương ứng
5. Render component phù hợp

**Template Logic:**
```vue
<template>
  <!-- Home view -->
  <div v-if="currentView === 'home'">
    <!-- Navigation cards -->
  </div>
  
  <!-- Customer list view -->
  <CustomerList v-else-if="currentView === 'customer_list'" />
  
  <!-- Customer edit view -->
  <CustomerEdit v-else-if="currentView === 'customer_edit'" />
</template>
```

---

## Flow Tạo Mới Customer

### Scenario: User Click "Doctype new customer" → Tạo Customer Mới

### Bước 1: Navigation từ Home

**File:** `frontend/src/App.vue`

```vue
<button @click="go('/feature1')">
  <h5>Doctype new customer</h5>
</button>
```

```javascript
go(href) {
  window.location.href = href;  // Navigate to /feature1
}
```

**Flow:**
1. User click button "Doctype new customer"
2. Trigger `@click="go('/feature1')"`
3. `go()` method set `window.location.href = '/feature1'`
4. Browser navigate đến `/feature1`

---

### Bước 2: Load Page `/feature1`

**File:** `www/feature1.html`

```html
{% block page_content %}
<div id="vue-app"></div>
{% endblock %}
{% block script %}
<script src="/assets/custom_app/frontend/js/main.js"></script>
{% endblock %}
```

**Flow:**
1. Frappe detect route `/feature1` → load `www/feature1.html`
2. Template render `<div id="vue-app"></div>`
3. Load Vue app script
4. Vue app mount lại (hoặc detect route change)

---

### Bước 3: App.vue Detect Route

**File:** `frontend/src/App.vue`

```javascript
initializeView() {
  const path = window.location.pathname;  // '/feature1'
  
  if (path.startsWith('/feature1')) {
    this.currentView = 'customer_list';  // ✅ Set view
    return;
  }
}
```

**Flow:**
1. `App.vue` detect path = `/feature1`
2. Set `currentView = 'customer_list'`
3. Template render `<CustomerList />` component

---

### Bước 4: CustomerList Component Mount

**File:** `frontend/src/components/CustomerList.vue`

```javascript
mounted() {
  this.loadCustomers();  // Tự động load danh sách khi mount
}
```

**Flow:**
1. `CustomerList` component mount
2. Tự động gọi `loadCustomers()` để load danh sách hiện có

---

### Bước 5: Load Danh Sách Customers

**File:** `frontend/src/components/CustomerList.vue`

```javascript
async loadCustomers() {
  this.loading = true;
  
  const r = await frappe.call({
    method: 'custom_app.customdemo.doctype.customer.customer.get_customers',
  });
  
  this.allCustomers = r.message || [];
  this.loading = false;
}
```

**Backend:** `customdemo/doctype/customer/customer.py`

```python
@frappe.whitelist(allow_guest=False)
def get_customers():
    return frappe.get_all(
        "Customer",
        fields=["name", "customer_name", "email", "phone", "role", "address"],
        order_by="modified desc",
        limit=50,
    )
```

**Flow Backend:**
1. Frontend gọi `frappe.call({method: 'get_customers'})`
2. Frappe route request đến `customer.get_customers()`
3. Backend execute `frappe.get_all()` → Query database
4. SQL: `SELECT name, customer_name, email, phone, role, address FROM tabCustomer ORDER BY modified DESC LIMIT 50`
5. Return JSON array về frontend

**Flow Frontend:**
1. Receive response → `r.message` = array of customers
2. Update `this.allCustomers = r.message`
3. Computed property `filteredCustomers` tự động update
4. Table re-render với data mới
5. Set `loading = false`

---

### Bước 6: User Điền Form và Submit

**File:** `frontend/src/components/CustomerList.vue`

```vue
<form @submit.prevent="handleSubmit">
  <input v-model.trim="form.customer_name" required />
  <input v-model.trim="form.email" />
  <input v-model.trim="form.phone" />
  <select v-model="form.role">...</select>
  <textarea v-model.trim="form.address"></textarea>
  <button type="submit">Save</button>
</form>
```

**Flow:**
1. User điền form (v-model bind data vào `this.form`)
2. Click "Save" → Trigger `@submit.prevent="handleSubmit"`
3. `prevent` ngăn form submit mặc định

---

### Bước 7: Validate và Gọi API Create

**File:** `frontend/src/components/CustomerList.vue`

```javascript
async handleSubmit() {
  // 1. Validate
  const customer_name = this.form.customer_name.trim();
  if (!customer_name) {
    this.showFormMessage('Name is required.', 'danger');
    return;
  }
  
  // 2. Prepare payload
  const payload = {
    customer_name,
    email: this.form.email.trim(),
    phone: this.form.phone.trim(),
    role: this.form.role,
    address: this.form.address.trim(),
  };
  
  // 3. Call API
  const r = await frappe.call({
    method: 'custom_app.customdemo.doctype.customer.customer.create_customer',
    args: payload,
  });
  
  // 4. Handle response
  if (r.message.success) {
    this.form = {};  // Reset form
    this.loadCustomers();  // Reload list
  }
}
```

**Flow:**
1. Validate `customer_name` required
2. Nếu invalid → Show error message → Return
3. Nếu valid → Prepare payload object
4. Call API `create_customer` với payload
5. Show loading message: "Saving..."

---

### Bước 8: Backend Xử Lý Create

**File:** `customdemo/doctype/customer/customer.py`

```python
@frappe.whitelist(allow_guest=False)
def create_customer(customer_name, email=None, phone=None, role=None, address=None):
    # 1. Tạo document object
    doc = frappe.get_doc({
        "doctype": "Customer",
        "customer_name": customer_name,
        "email": email,
        "phone": phone,
        "role": role,
        "address": address,
    })
    
    # 2. Insert → Tự động gọi validate()
    doc.insert()
    
    # 3. Commit transaction
    frappe.db.commit()
    
    # 4. Return success
    return {"success": True, "name": doc.name}
```

**Flow Chi Tiết:**

**a) Tạo Document Object:**
```python
doc = frappe.get_doc({
    "doctype": "Customer",
    "customer_name": "John Doe",
    "email": "john@example.com",
    ...
})
```
- Tạo Python object đại diện cho Customer document
- Chưa lưu vào database

**b) Insert Document:**
```python
doc.insert()
```

**Flow trong `insert()`:**
1. Frappe tự động gọi `Customer.validate()`
2. `validate()` check:
   ```python
   if not self.email and not self.phone:
       frappe.throw("Vui lòng nhập Email hoặc Phone")
   if self.email and '@' not in self.email:
       frappe.throw("Email không hợp lệ")
   ```
3. Nếu validate fail → Throw exception → Return error về frontend
4. Nếu validate pass → Continue
5. Frappe tự động gọi `before_save()` (nếu có)
6. Insert vào database: `INSERT INTO tabCustomer (...) VALUES (...)`
7. Frappe tự động gọi `after_insert()` (nếu có)
8. Generate `name` (ví dụ: "CUST-00001")

**c) Commit Transaction:**
```python
frappe.db.commit()
```
- Commit transaction vào database
- Đảm bảo data được lưu vĩnh viễn

**d) Return Response:**
```python
return {"success": True, "name": doc.name}
```
- Return JSON về frontend

---

### Bước 9: Frontend Nhận Response

**File:** `frontend/src/components/CustomerList.vue`

```javascript
const r = await frappe.call({...});

if (r && r.message && r.message.success) {
  // Success
  this.showFormMessage('Saved successfully!', 'success');
  this.form = {};  // Reset form
  this.loadCustomers();  // Reload danh sách
} else {
  // Error
  this.showFormMessage('Error saving customer.', 'danger');
}
```

**Flow:**
1. Receive response từ backend
2. Check `r.message.success === true`
3. Nếu success:
   - Show success message
   - Reset form: `this.form = {}`
   - Reload danh sách: `this.loadCustomers()`
4. Nếu error:
   - Show error message

---

### Bước 10: Reload Danh Sách

**File:** `frontend/src/components/CustomerList.vue`

```javascript
this.loadCustomers();
```

**Flow:**
1. Gọi lại `loadCustomers()`
2. Call API `get_customers()`
3. Backend query database → Return danh sách mới (bao gồm customer vừa tạo)
4. Update `this.allCustomers`
5. Table tự động re-render với customer mới

---

## Flow Xem Danh Sách Customer

### Scenario: User vào trang `/feature1` để xem danh sách

### Bước 1-3: Giống như "Flow Tạo Mới" (Navigation → Mount → Load)

### Bước 4: Render Table với Data

**File:** `frontend/src/components/CustomerList.vue`

```vue
<tbody>
  <tr v-if="loading">
    <td colspan="6">Loading...</td>
  </tr>
  <tr v-else-if="filteredCustomers.length === 0">
    <td colspan="6">No customers yet.</td>
  </tr>
  <tr v-else v-for="customer in filteredCustomers" :key="customer.name">
    <td>{{ customer.customer_name }}</td>
    <td>{{ customer.email }}</td>
    <td>{{ customer.phone }}</td>
    <td>{{ customer.role }}</td>
    <td>{{ customer.address }}</td>
    <td>
      <button @click="handleEdit(customer.name)">Edit</button>
      <button @click="handleDelete(customer.name)">Delete</button>
    </td>
  </tr>
</tbody>
```

**Flow:**
1. Component render template
2. Check `loading`:
   - `true` → Show "Loading..."
   - `false` → Continue
3. Check `filteredCustomers.length`:
   - `0` → Show "No customers yet."
   - `> 0` → Render table rows
4. `v-for` loop qua `filteredCustomers`
5. Render mỗi customer thành 1 table row
6. Bind Edit/Delete buttons với handlers

**Computed Property:**
```javascript
computed: {
  filteredCustomers() {
    // Tự động re-calculate khi filterSearch/filterRole thay đổi
    let filtered = this.allCustomers.slice();
    
    // Apply filters...
    return filtered;
  }
}
```

---

## Flow Chỉnh Sửa Customer

### Scenario: User Click "Edit" → Chỉnh sửa Customer

### Bước 1: Click Edit Button

**File:** `frontend/src/components/CustomerList.vue`

```javascript
handleEdit(name) {
  window.location.href = '/feature1_edit?name=' + encodeURIComponent(name);
}
```

**Flow:**
1. User click "Edit" button
2. Trigger `@click="handleEdit(customer.name)"`
3. `customer.name` = "CUST-00001" (docname)
4. Navigate to `/feature1_edit?name=CUST-00001`

---

### Bước 2: Load Edit Page

**File:** `www/feature1_edit.html`

```html
{% block page_content %}
<div id="vue-app"></div>
{% endblock %}
```

**Flow:**
1. Browser navigate → Frappe load `www/feature1_edit.html`
2. Vue app mount
3. `App.vue` detect route

---

### Bước 3: App.vue Detect Edit Route

**File:** `frontend/src/App.vue`

```javascript
initializeView() {
  const path = window.location.pathname;  // '/feature1_edit'
  const params = new URLSearchParams(window.location.search);
  
  if (path.startsWith('/feature1_edit')) {
    const name = params.get('name');  // 'CUST-00001'
    if (name) {
      this.editCustomerName = name;
      this.currentView = 'customer_edit';
      return;
    }
  }
}
```

**Flow:**
1. Detect path = `/feature1_edit`
2. Extract query parameter `name` = "CUST-00001"
3. Set `editCustomerName = "CUST-00001"`
4. Set `currentView = 'customer_edit'`
5. Render `<CustomerEdit :customer-name="editCustomerName" />`

---

### Bước 4: CustomerEdit Component Mount

**File:** `frontend/src/components/CustomerEdit.vue`

```javascript
props: {
  customerName: {
    type: String,
    required: true,
  },
}

mounted() {
  if (!this.customerName) {
    window.location.href = '/feature1';
    return;
  }
  
  this.loadCustomer();  // Load customer data
}
```

**Flow:**
1. Component nhận prop `customerName = "CUST-00001"`
2. Check prop có giá trị
3. Nếu không có → Redirect về `/feature1`
4. Nếu có → Gọi `loadCustomer()`

---

### Bước 5: Load Customer Data

**File:** `frontend/src/components/CustomerEdit.vue`

```javascript
async loadCustomer() {
  this.message = 'Loading customer...';
  this.loading = true;
  
  const r = await frappe.call({
    method: 'custom_app.customdemo.doctype.customer.customer.get_customer',
    args: { name: this.customerName },
  });
  
  if (r && r.message) {
    const c = r.message;
    // Populate form
    this.form.customer_name = c.customer_name || '';
    this.form.email = c.email || '';
    this.form.phone = c.phone || '';
    this.form.role = c.role || '';
    this.form.address = c.address || '';
  }
  
  this.loading = false;
}
```

**Backend:** `customdemo/doctype/customer/customer.py`

```python
@frappe.whitelist(allow_guest=False)
def get_customer(name: str):
    doc = frappe.get_doc("Customer", name)
    return doc.as_dict()
```

**Flow Backend:**
1. Frontend gọi `get_customer(name="CUST-00001")`
2. Backend: `frappe.get_doc("Customer", "CUST-00001")`
3. SQL: `SELECT * FROM tabCustomer WHERE name = 'CUST-00001'`
4. Return document as dictionary

**Flow Frontend:**
1. Receive customer data
2. Populate form fields với data
3. User có thể edit

---

### Bước 6: User Edit và Submit

**File:** `frontend/src/components/CustomerEdit.vue`

```javascript
async handleSubmit() {
  // Validate
  if (!this.form.customer_name.trim()) {
    this.message = 'Name is required.';
    return;
  }
  
  // Prepare payload
  const payload = {
    name: this.customerName,
    customer_name: this.form.customer_name,
    email: this.form.email,
    phone: this.form.phone,
    role: this.form.role,
    address: this.form.address,
  };
  
  // Call API
  const r = await frappe.call({
    method: 'custom_app.customdemo.doctype.customer.customer.update_customer',
    args: payload,
  });
  
  // Success → Redirect
  if (r.message.success) {
    this.message = 'Updated successfully! Redirecting...';
    setTimeout(() => {
      window.location.href = '/feature1';
    }, 1000);
  }
}
```

---

### Bước 7: Backend Update

**File:** `customdemo/doctype/customer/customer.py`

```python
@frappe.whitelist(allow_guest=False)
def update_customer(name: str, customer_name=None, email=None, ...):
    # 1. Load existing document
    doc = frappe.get_doc("Customer", name)
    
    # 2. Update fields
    if customer_name is not None:
        doc.customer_name = customer_name
    if email is not None:
        doc.email = email
    # ...
    
    # 3. Save → Tự động gọi validate()
    doc.save()
    
    # 4. Commit
    frappe.db.commit()
    
    return {"success": True, "name": doc.name}
```

**Flow:**
1. Load document từ database
2. Update các fields được truyền vào
3. `doc.save()` → Tự động gọi `validate()`
4. Nếu validate pass → Update database: `UPDATE tabCustomer SET ... WHERE name = ...`
5. Commit transaction
6. Return success

---

### Bước 8: Redirect về List

**File:** `frontend/src/components/CustomerEdit.vue`

```javascript
if (r.message.success) {
  this.message = 'Updated successfully! Redirecting...';
  setTimeout(() => {
    window.location.href = '/feature1';  // Redirect sau 1 giây
  }, 1000);
}
```

**Flow:**
1. Show success message
2. Đợi 1 giây
3. Redirect về `/feature1`
4. Danh sách tự động reload và hiển thị data đã update

---

## Flow Xóa Customer

### Scenario: User Click "Delete" → Xóa Customer

### Bước 1: Click Delete Button

**File:** `frontend/src/components/CustomerList.vue`

```javascript
async handleDelete(name) {
  // 1. Confirm
  if (!confirm('Bạn có chắc chắn muốn xóa customer này không?')) {
    return;  // User cancel
  }
  
  // 2. Show loading
  this.showListMessage('Deleting...', 'info');
  
  // 3. Call API
  const r = await frappe.call({
    method: 'custom_app.customdemo.doctype.customer.customer.delete_customer',
    args: { name },
  });
  
  // 4. Handle response
  if (r.message.success) {
    this.showListMessage('Deleted successfully.', 'success');
    this.loadCustomers();  // Reload list
  }
}
```

**Flow:**
1. User click "Delete" button
2. Show confirm dialog
3. Nếu user cancel → Return (không làm gì)
4. Nếu user confirm → Continue
5. Show loading message: "Deleting..."
6. Call API `delete_customer(name)`

---

### Bước 2: Backend Delete

**File:** `customdemo/doctype/customer/customer.py`

```python
@frappe.whitelist(allow_guest=False)
def delete_customer(name: str):
    frappe.delete_doc("Customer", name, ignore_permissions=False)
    frappe.db.commit()
    return {"success": True, "name": name}
```

**Flow:**
1. `frappe.delete_doc("Customer", "CUST-00001")`
2. SQL: `DELETE FROM tabCustomer WHERE name = 'CUST-00001'`
3. Commit transaction
4. Return success

---

### Bước 3: Reload List

**File:** `frontend/src/components/CustomerList.vue`

```javascript
if (r.message.success) {
  this.showListMessage('Deleted successfully.', 'success');
  this.loadCustomers();  // Reload danh sách
}
```

**Flow:**
1. Show success message
2. Gọi `loadCustomers()` để reload danh sách
3. Table tự động update (customer đã bị xóa không còn trong list)

---

## Flow Filter và Search

### Scenario: User Type vào Search Box hoặc Chọn Role Filter

### Bước 1: User Input

**File:** `frontend/src/components/CustomerList.vue`

```vue
<input
  v-model.trim="filterSearch"
  placeholder="Search by name, email, phone, address..."
/>
<select v-model="filterRole">
  <option value="">All roles</option>
  <option value="Customer">Customer</option>
  <option value="VIP">VIP</option>
  <option value="Partner">Partner</option>
</select>
```

**Flow:**
1. User type vào search box → `v-model` update `filterSearch`
2. User chọn role → `v-model` update `filterRole`
3. Vue reactive system detect change

---

### Bước 2: Computed Property Re-calculate

**File:** `frontend/src/components/CustomerList.vue`

```javascript
computed: {
  filteredCustomers() {
    // Tự động chạy lại khi filterSearch hoặc filterRole thay đổi
    let filtered = this.allCustomers.slice();  // Copy array
    
    // Search filter
    const keyword = this.filterSearch.toLowerCase().trim();
    if (keyword) {
      filtered = filtered.filter(c => {
        const values = [
          c.customer_name,
          c.email,
          c.phone,
          c.address,
        ].map(v => (v || '').toLowerCase());
        
        return values.some(v => v.includes(keyword));
      });
    }
    
    // Role filter
    const role = this.filterRole.trim();
    if (role) {
      filtered = filtered.filter(c => (c.role || '') === role);
    }
    
    return filtered;  // Return filtered array
  }
}
```

**Flow:**
1. `filterSearch` hoặc `filterRole` thay đổi
2. Vue detect dependency change
3. Tự động re-calculate `filteredCustomers()`
4. Apply search filter (nếu có keyword)
5. Apply role filter (nếu có role)
6. Return filtered array

---

### Bước 3: Table Re-render

**File:** `frontend/src/components/CustomerList.vue`

```vue
<tr v-for="customer in filteredCustomers" :key="customer.name">
  <!-- Table cells -->
</tr>
```

**Flow:**
1. `filteredCustomers` computed property return array mới
2. Vue detect change
3. `v-for` tự động re-render table rows
4. Chỉ hiển thị customers match với filter
5. **Không cần call API** - Filter hoàn toàn ở client-side

---

## Backend API Flow

### Tổng Quan API Methods

| Method | Endpoint | Mô Tả |
|--------|----------|-------|
| `get_customers` | `custom_app.customdemo.doctype.customer.customer.get_customers` | Lấy danh sách customers |
| `get_customer` | `custom_app.customdemo.doctype.customer.customer.get_customer` | Lấy chi tiết 1 customer |
| `create_customer` | `custom_app.customdemo.doctype.customer.customer.create_customer` | Tạo mới customer |
| `update_customer` | `custom_app.customdemo.doctype.customer.customer.update_customer` | Cập nhật customer |
| `delete_customer` | `custom_app.customdemo.doctype.customer.customer.delete_customer` | Xóa customer |

### API Call Flow

```
Frontend: frappe.call({method: '...', args: {...}})
    ↓
Frappe Framework: Route request
    ↓
Backend: customer.py method
    ↓
Frappe ORM: Database operation
    ↓
MySQL: Execute SQL
    ↓
Response: Return data
    ↓
Frontend: Receive response
```

### Document Lifecycle

Khi tạo hoặc update document, Frappe tự động chạy các hooks:

```
create_customer() / update_customer()
    ↓
doc.insert() / doc.save()
    ↓
validate()  ← Tự động gọi
    ↓
before_save()  ← Tự động gọi (nếu có)
    ↓
Database INSERT/UPDATE
    ↓
after_insert()  ← Tự động gọi (nếu có, chỉ khi insert)
```

---

## Frontend Component Flow

### Component Hierarchy

```
App.vue (Root)
    ├── Home View (v-if="currentView === 'home'")
    │   └── Navigation Cards
    │
    ├── CustomerList (v-else-if="currentView === 'customer_list'")
    │   ├── Form (Create Customer)
    │   └── Table (List Customers)
    │
    └── CustomerEdit (v-else-if="currentView === 'customer_edit'")
        └── Form (Edit Customer)
```

### Data Flow

```
App.vue
    ├── currentView (state)
    │   ├── 'home'
    │   ├── 'customer_list'
    │   └── 'customer_edit'
    │
CustomerList
    ├── allCustomers (data từ API)
    ├── filterSearch (user input)
    ├── filterRole (user input)
    └── filteredCustomers (computed)
        └── Tự động filter allCustomers
            └── Render table
```

### Event Flow

```
User Action
    ↓
Component Method
    ↓
API Call (frappe.call)
    ↓
Backend Process
    ↓
Response
    ↓
Update Component Data
    ↓
Re-render UI
```

---

## Tóm Tắt Flow Chính

### 1. Khởi Động
```
Browser → HTML Template → Vue App Mount → App.vue → Initialize View
```

### 2. Tạo Mới Customer
```
Click Button → Navigate → Load Page → Mount Component → 
Load List → Fill Form → Submit → API Call → Backend Validate → 
Insert DB → Response → Reset Form → Reload List
```

### 3. Chỉnh Sửa Customer
```
Click Edit → Navigate → Load Page → Mount Component → 
Load Customer Data → Populate Form → Edit → Submit → 
API Call → Backend Validate → Update DB → Response → Redirect
```

### 4. Xóa Customer
```
Click Delete → Confirm → API Call → Backend Delete → 
Response → Reload List
```

### 5. Filter/Search
```
User Input → v-model Update → Computed Re-calculate → 
Table Re-render (Client-side, không call API)
```

---

## Lưu Ý Quan Trọng

1. **Validation**: Có 2 lớp validation
   - Frontend: Basic validation (required fields)
   - Backend: Business logic validation (email/phone, format)

2. **Reactive System**: Vue.js tự động update UI khi data thay đổi
   - Computed properties tự động re-calculate
   - v-model tự động sync data

3. **API Calls**: Tất cả API calls đều async
   - Sử dụng `async/await` hoặc `.then()`
   - Cần handle error cases

4. **State Management**: 
   - Component-level state (không dùng Vuex/Pinia)
   - Data flow từ parent → child qua props
   - Events từ child → parent qua `$emit`

5. **Routing**: 
   - Không dùng Vue Router
   - Sử dụng URL-based routing với `window.location`
   - App.vue detect path và render component tương ứng

---

**Last Updated:** 2025-01-XX  
**Version:** 1.0.0  
**Author:** MH

