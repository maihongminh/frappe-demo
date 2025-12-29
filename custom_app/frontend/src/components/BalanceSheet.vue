<template>
	<div class="balance-sheet-container">
		<div class="header-section">
			<button class="btn btn-secondary mb-3" @click="$emit('back')">
				← Quay lại
			</button>
			<h2 class="mb-4">Bảng cân đối kế toán</h2>
			
			<!-- Form filters: fiscal year, currency, circular template -->
			<div class="filters-section mb-3">
				<div class="row g-3">
					<div class="col-md-3">
						<label for="fiscalYear" class="form-label">Năm tài chính</label>
						<select id="fiscalYear" class="form-select" v-model="fiscalYear" :disabled="isEditing">
							<option value="2023">2023</option>
							<option value="2024">2024</option>
							<option value="2025">2025</option>
							<option value="2026">2026</option>
						</select>
					</div>
					<div class="col-md-3">
						<label for="currency" class="form-label">Loại tiền tệ</label>
						<select id="currency" class="form-select" v-model="currency" :disabled="isEditing">
							<option value="VND">Việt Nam Đồng</option>
							<option value="USD">USD</option>
							<option value="EUR">EUR</option>
						</select>
					</div>
					<div class="col-md-3">
						<label for="circularTemplate" class="form-label">Mẫu thông tư</label>
						<select id="circularTemplate" class="form-select" v-model="circularTemplate" :disabled="isEditing">
							<option value="200">Thông tư 200</option>
							<option value="133">Thông tư 133</option>
							<option value="other">Khác</option>
						</select>
					</div>
					<div class="col-md-3 d-flex align-items-end">
						<button class="btn btn-info w-100" @click="loadBalanceSheet" :disabled="isEditing">
							Tải dữ liệu
						</button>
					</div>
				</div>
			</div>

			<div class="toolbar mb-3">
				<button 
					v-if="!isEditing" 
					class="btn btn-primary"
					@click="enableEdit"
				>
					Chỉnh sửa
				</button>
				<template v-else>
					<button class="btn btn-success me-2" @click="saveChanges">
						Lưu
					</button>
					<button class="btn btn-secondary" @click="cancelEdit">
						Hủy
					</button>
				</template>
			</div>
		</div>

		<div class="table-responsive">
			<table class="table table-bordered balance-sheet-table">
				<thead>
					<tr class="table-primary">
						<th style="width: 5%">Chỉ tiêu</th>
						<th style="width: 8%">Mã số</th>
						<th style="width: 8%">Thuyết minh</th>
						<th style="width: 15%">Số đầu năm</th>
						<th style="width: 15%">Số cuối năm</th>
					</tr>
					<tr class="table-info">
						<th>1</th>
						<th>2</th>
						<th>3</th>
						<th>4</th>
						<th>5</th>
					</tr>
				</thead>
				<tbody>
					<!-- Tài sản -->
					<tr class="section-header">
						<td colspan="5"><strong>Tài sản</strong></td>
					</tr>
					
					<tr v-for="row in assetRows" :key="row.id" :class="{ 'indent-1': row.indent === 1, 'indent-2': row.indent === 2 }">
						<td>{{ row.label }}</td>
						<td>
							<input 
								v-if="isEditing" 
								type="text" 
								v-model="row.code" 
								class="form-control form-control-sm"
							/>
							<span v-else>{{ row.code }}</span>
						</td>
						<td>
							<input 
								v-if="isEditing" 
								type="text" 
								v-model="row.note" 
								class="form-control form-control-sm"
							/>
							<span v-else>{{ row.note }}</span>
						</td>
						<td>
							<input 
								v-if="isEditing" 
								type="number" 
								v-model="row.startYear" 
								class="form-control form-control-sm text-end"
							/>
							<span v-else class="number-cell">{{ formatNumber(row.startYear) }}</span>
						</td>
						<td>
							<input 
								v-if="isEditing" 
								type="number" 
								v-model="row.endYear" 
								class="form-control form-control-sm text-end"
							/>
							<span v-else class="number-cell">{{ formatNumber(row.endYear) }}</span>
						</td>
					</tr>

					<!-- Nguồn vốn -->
					<tr class="section-header">
						<td colspan="5"><strong>Nguồn vốn</strong></td>
					</tr>
					
					<tr v-for="row in equityRows" :key="row.id" :class="{ 'indent-1': row.indent === 1, 'indent-2': row.indent === 2 }">
						<td>{{ row.label }}</td>
						<td>
							<input 
								v-if="isEditing" 
								type="text" 
								v-model="row.code" 
								class="form-control form-control-sm"
							/>
							<span v-else>{{ row.code }}</span>
						</td>
						<td>
							<input 
								v-if="isEditing" 
								type="text" 
								v-model="row.note" 
								class="form-control form-control-sm"
							/>
							<span v-else>{{ row.note }}</span>
						</td>
						<td>
							<input 
								v-if="isEditing" 
								type="number" 
								v-model="row.startYear" 
								class="form-control form-control-sm text-end"
							/>
							<span v-else class="number-cell">{{ formatNumber(row.startYear) }}</span>
						</td>
						<td>
							<input 
								v-if="isEditing" 
								type="number" 
								v-model="row.endYear" 
								class="form-control form-control-sm text-end"
							/>
							<span v-else class="number-cell">{{ formatNumber(row.endYear) }}</span>
						</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
</template>

<script>
export default {
	name: 'BalanceSheet',
	emits: ['back'],
	data() {
		return {
			fiscalYear: '2025',
			currency: 'VND',
			circularTemplate: '200',
			isEditing: false,
			assetRows: [
				{ id: 'a1', label: 'I. Tiền và các khoản tương đương tiền', code: '110', note: '', startYear: 0, endYear: 0, indent: 0, parentId: null },
				{ id: 'a2', label: 'II. Đầu tư tài chính', code: '120', note: '', startYear: 0, endYear: 0, indent: 0, parentId: null },
				{ id: 'a3', label: '1 Chứng khoán kinh doanh', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'a2' },
				{ id: 'a4', label: '2 Đầu tư nắm giữ đến ngày đáo hạn', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'a2' },
				{ id: 'a5', label: '3 Đầu tư góp vốn vào đơn vị khác', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'a2' },
				{ id: 'a6', label: '4 Dự phòng tổn thất đầu tư tài chính (*)', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'a2' },
				{ id: 'a7', label: 'III. Các khoản phải thu', code: '120', note: '', startYear: 0, endYear: 0, indent: 0, parentId: null },
				{ id: 'a8', label: '1 Phải thu của khách hàng', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'a7' },
				{ id: 'a9', label: '2 Trả trước cho người bán', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'a7' },
				{ id: 'a10', label: '3 Vốn kinh doanh ở đơn vị trực thuộc', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'a7' },
				{ id: 'a11', label: '4 Phải thu khác', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'a7' },
				{ id: 'a12', label: '5 Tài sản thiếu chờ xử lý', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'a7' },
				{ id: 'a13', label: '6 Dự phòng phải thu khó đòi (*)', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'a7' },
				{ id: 'a14', label: 'IV. Hàng tồn kho', code: '12', note: '', startYear: 0, endYear: 0, indent: 0, parentId: null },
				{ id: 'a15', label: '1 Hàng tồn kho', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'a14' },
				{ id: 'a16', label: '2 Dự phòng giảm giá hàng tồn kho (*)', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'a14' },
				{ id: 'a17', label: 'V. Tài sản cố định', code: '12', note: '', startYear: 0, endYear: 0, indent: 0, parentId: null },
				{ id: 'a18', label: '1 Nguyên giá', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'a17' },
				{ id: 'a19', label: '2 Giá trị hao mòn lũy kế (*)', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'a17' },
				{ id: 'a20', label: 'VI. Bất động sản đầu tư', code: '12', note: '', startYear: 0, endYear: 0, indent: 0, parentId: null },
				{ id: 'a21', label: '1 Nguyên giá', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'a20' },
				{ id: 'a22', label: '2 Giá trị hao mòn lũy kế (*)', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'a20' },
				{ id: 'a23', label: 'VII. XDCB dở dang', code: '12', note: '', startYear: 0, endYear: 0, indent: 0, parentId: null },
				{ id: 'a24', label: 'VIII. Tài sản khác', code: '12', note: '', startYear: 0, endYear: 0, indent: 0, parentId: null },
				{ id: 'a25', label: '1 Thuế GTGT được khấu trừ', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'a24' },
				{ id: 'a26', label: '2 Tài sản khác', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'a24' },
				{ id: 'a27', label: 'TỔNG CỘNG TÀI SẢN (200 = 110+120+130+140+150+160+170+180)', code: '200', note: '', startYear: 0, endYear: 0, indent: 0, parentId: null },
			],
			equityRows: [
				{ id: 'e1', label: 'I. Nợ phải trả', code: '300', note: '', startYear: 0, endYear: 0, indent: 0, parentId: null },
				{ id: 'e2', label: '1 Phải trả người bán', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'e1' },
				{ id: 'e3', label: '2 Người mua trả tiền trước', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'e1' },
				{ id: 'e4', label: '3 Thuế và các khoản phải nộp Nhà nước', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'e1' },
				{ id: 'e5', label: '4 Phải trả người lao động', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'e1' },
				{ id: 'e6', label: '5 Phải trả khác', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'e1' },
				{ id: 'e7', label: '6 Phải trả khác', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'e1' },
				{ id: 'e8', label: '7 Phải trả nội bộ về vốn kinh doanh', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'e1' },
				{ id: 'e9', label: '8 Dự phòng phải trả', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'e1' },
				{ id: 'e10', label: '9 Quỹ khen thưởng, phúc lợi', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'e1' },
				{ id: 'e11', label: '10 Quỹ phát triển khoa học và công nghệ', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'e1' },
				{ id: 'e12', label: 'II Vốn chủ sở hữu', code: '300', note: '', startYear: 0, endYear: 0, indent: 0, parentId: null },
				{ id: 'e13', label: '1 Vốn góp của chủ sở hữu', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'e12' },
				{ id: 'e14', label: '2 Thặng dư vốn cổ phần', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'e12' },
				{ id: 'e15', label: '3 Vốn khác của chủ sở hữu', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'e12' },
				{ id: 'e16', label: '4 Cổ phiếu quỹ (*)', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'e12' },
				{ id: 'e17', label: '5 Chênh lệch tỷ giá hối đoái', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'e12' },
				{ id: 'e18', label: '6 Các quỹ thuộc vốn chủ sở hữu', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'e12' },
				{ id: 'e19', label: '7 Lợi nhuận sau thuế chưa phân phối', code: '12', note: '', startYear: 0, endYear: 0, indent: 1, parentId: 'e12' },
				{ id: 'e20', label: 'TỔNG CỘNG NGUỒN VỐN (500 = 300 + 400)', code: '300', note: '', startYear: 0, endYear: 0, indent: 0, parentId: null },
			],
			backupData: null,
		};
	},
	methods: {
		async loadBalanceSheet() {
			try {
				const csrfToken = window.getCSRFToken ? window.getCSRFToken() : (window.csrf_token || '');
				const response = await fetch(
					`/api/method/custom_app.customdemo.doctype.balance_sheet.balance_sheet.get_balance_sheet_by_filters?fiscal_year=${this.fiscalYear}&circular_template=${this.circularTemplate}`,
					{
						method: 'GET',
						headers: {
							'Content-Type': 'application/json',
							'X-Frappe-CSRF-Token': csrfToken,
						},
						credentials: 'include',
					}
				);
				const result = await response.json();
				
				if (result.message && result.message.success) {
					const data = result.message.data;
					const parsedData = data.parsed_data;
					
					if (parsedData) {
						// Load assets and equity from parsed data
						if (parsedData.assets && Array.isArray(parsedData.assets)) {
							this.assetRows = parsedData.assets;
						}
						if (parsedData.equity && Array.isArray(parsedData.equity)) {
							this.equityRows = parsedData.equity;
						}
						alert(`Đã tải dữ liệu: ${data.title}`);
					} else {
						alert('Không tìm thấy dữ liệu trong bảng cân đối này.');
					}
				} else {
					alert(result.message?.message || 'Không tìm thấy bảng cân đối kế toán phù hợp');
				}
			} catch (err) {
				console.error('Error loading balance sheet:', err);
				alert('Lỗi khi tải dữ liệu. Vui lòng xem Console.');
			}
		},
		enableEdit() {
			this.isEditing = true;
			// Backup current data
			this.backupData = {
				assetRows: JSON.parse(JSON.stringify(this.assetRows)),
				equityRows: JSON.parse(JSON.stringify(this.equityRows)),
			};
		},
		async saveChanges() {
			// Chuyển data thành JSON
			const jsonData = {
				title: `Bảng cân đối kế toán ${this.fiscalYear} - ${this.circularTemplate}`,
				fiscal_year: this.fiscalYear,
				currency: this.currency,
				circular_template: this.circularTemplate,
				timestamp: new Date().toISOString(),
				data: {
					assets: this.assetRows,
					equity: this.equityRows,
				}
			};

			// 1) Vẫn trả ra chuỗi JSON (log/alert) như yêu cầu
			const jsonString = JSON.stringify(jsonData, null, 2);
			console.log('Balance Sheet JSON:', jsonString);

			// 2) Gửi data JSON đó lên API Frappe để backend lưu DB
			try {
				const csrfToken = window.getCSRFToken ? window.getCSRFToken() : (window.csrf_token || '');
				const response = await fetch('/api/method/custom_app.customdemo.doctype.balance_sheet.balance_sheet.save_balance_sheet', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'X-Frappe-CSRF-Token': csrfToken,
					},
					credentials: 'include',
					body: JSON.stringify({ payload: JSON.stringify(jsonData) }),
				});
				const data = await response.json();
				if (!(response.ok && data.message && data.message.success)) {
					console.error('Save Balance Sheet failed:', data);
					alert('Lưu JSON thành công (log console) nhưng lưu DB thất bại. Vui lòng xem Console/Network.');
				} else {
					// thành công -> trả docname để tiện trace
					alert(`Đã lưu thành công!\n\nDocname: ${data.message.name}\n\nJSON đã được log ra Console (F12)`);
				}
			} catch (err) {
				console.error('Error calling save_balance_sheet API:', err);
				alert('Lưu JSON thành công (log console) nhưng gọi API lưu DB bị lỗi.');
			}

			// Tắt chế độ edit
			this.isEditing = false;
			this.backupData = null;

			// Tùy chọn: Lưu vào localStorage
			localStorage.setItem('balanceSheetData', JSON.stringify(jsonData));
		},
		cancelEdit() {
			// Restore backup
			if (this.backupData) {
				this.assetRows = this.backupData.assetRows;
				this.equityRows = this.backupData.equityRows;
			}
			this.isEditing = false;
			this.backupData = null;
		},
		formatNumber(value) {
			if (!value || value === 0) return '0';
			return Number(value).toLocaleString('vi-VN');
		},
	},
};
</script>

<style scoped>
.balance-sheet-container {
	padding: 20px;
	max-width: 1400px;
	margin: 0 auto;
}

.header-section {
	margin-bottom: 20px;
}

.toolbar {
	display: flex;
	gap: 10px;
}

.balance-sheet-table {
	font-size: 14px;
}

.balance-sheet-table thead th {
	text-align: center;
	vertical-align: middle;
	background-color: #e3f2fd;
}

.balance-sheet-table .section-header {
	background-color: #f5f5f5;
	font-weight: bold;
}

.balance-sheet-table .indent-1 td:first-child {
	padding-left: 30px;
}

.balance-sheet-table .indent-2 td:first-child {
	padding-left: 50px;
}

.balance-sheet-table td {
	vertical-align: middle;
}

.number-cell {
	display: block;
	text-align: right;
	font-family: monospace;
}

.form-control-sm {
	padding: 4px 8px;
	font-size: 13px;
}

input[type="number"].form-control-sm {
	text-align: right;
}

.table-responsive {
	overflow-x: auto;
}
</style>
