<template>
	<div class="balance-sheet-container">
		<div class="header-section">
			<button class="btn btn-secondary mb-3" @click="$emit('back')">
				← Quay lại
			</button>
			<h2 class="mb-4">Bảng cân đối kế toán</h2>
			
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
		enableEdit() {
			this.isEditing = true;
			// Backup current data
			this.backupData = {
				assetRows: JSON.parse(JSON.stringify(this.assetRows)),
				equityRows: JSON.parse(JSON.stringify(this.equityRows)),
			};
		},
		saveChanges() {
			// Chuyển data thành JSON
			const jsonData = {
				timestamp: new Date().toISOString(),
				data: {
					assets: this.assetRows,
					equity: this.equityRows,
				}
			};

			// Log JSON ra console
			console.log('Balance Sheet JSON:', JSON.stringify(jsonData, null, 2));

			// Hiển thị JSON trong alert (tùy chọn)
			alert('Đã lưu thành công!\n\nJSON data đã được log ra Console (F12)');

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
