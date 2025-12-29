frappe.ui.form.on('Customer', {
	// Hook chạy khi form load/reload
	refresh: function (frm) {
		
		// frm.doc: Object chứa dữ liệu của document (các field)
		// Các phương thức thường dùng:
		// - frm.set_value('fieldname', value): Set giá trị cho field
		// - frm.get_value('fieldname'): Lấy giá trị của field
		// - frm.refresh_field('fieldname'): Refresh field
		// - frm.save(): Lưu document
		// - frm.add_custom_button('Label', function() {}): Thêm button tùy chỉnh
		
		// Thêm nút xóa customer
		if (!frm.is_new()) {
			frm.add_custom_button('Xóa Customer', function() {
				frappe.confirm(
					'Bạn có chắc chắn muốn xóa customer "' + frm.doc.customer_name + '" không?',
					function() {
						// khi click vào yes
						frappe.call({
							method: 'custom_app.custom_app.customdemo.doctype.customer.customer.delete_customer',
							args: {
								name: frm.doc.name
							},
							callback: function(r) {
								if (r.message && r.message.success) {
									frappe.show_alert({
										message: 'Đã xóa customer thành công',
										indicator: 'green'
									}, 3);
									// Chuyển về list view
									frappe.set_route('List', 'Customer');
								}
							},
							error: function(r) {
								frappe.show_alert({
									message: 'Có lỗi xảy ra khi xóa customer',
									indicator: 'red'
								}, 5);
							}
						});
					}
				);
			});
		}
	},
	
	validate: function(frm) {
		// frm.doc: Truy cập dữ liệu của document
		
		// kiểm tra mail,phone
		if (!frm.doc.email && !frm.doc.phone) {
			frappe.throw('Vui lòng nhập Email hoặc Phone');
		}
		
		// email format
		if (frm.doc.email && !frm.doc.email.includes('@')) {
			frappe.throw('Email không hợp lệ');
		}
	},
	
});
