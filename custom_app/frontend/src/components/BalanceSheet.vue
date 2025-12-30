<template>
	<div class="balance-sheet-container">
		<div class="header-section">
			<button class="btn btn-secondary mb-3" @click="$emit('back')">
				← Quay lại
			</button>
			<h2 class="mb-4">{{ reportTitle }}</h2>
			
			<!-- Form filters: circular template, report type, fiscal year, currency -->
			<div class="filters-section mb-3">
				<div class="row g-3">
					<div class="col-md-3">
						<label for="circularTemplate" class="form-label">Thông tư</label>
						<select id="circularTemplate" class="form-select" v-model="selectedCircularTemplate" :disabled="isEditing" @change="onCircularTemplateChange">
							<option v-for="ct in circularTemplatesList" :key="ct.code" :value="ct.code">
								{{ ct.template_name }}
							</option>
						</select>
					</div>
					<div class="col-md-3">
						<label for="reportType" class="form-label">Loại báo cáo</label>
						<select id="reportType" class="form-select" v-model="reportType" :disabled="isEditing" @change="onReportTypeChange">
							<option v-for="rt in filteredReportTypes" :key="rt.code" :value="rt.code">
								{{ rt.report_name }}
							</option>
						</select>
					</div>
					<div class="col-md-2">
						<label for="fiscalYear" class="form-label">Năm tài chính</label>
						<select id="fiscalYear" class="form-select" v-model="fiscalYear" :disabled="isEditing">
							<option value="2023">2023</option>
							<option value="2024">2024</option>
							<option value="2025">2025</option>
							<option value="2026">2026</option>
						</select>
					</div>
					<div class="col-md-2">
						<label for="currency" class="form-label">Loại tiền tệ</label>
						<select id="currency" class="form-select" v-model="currency" :disabled="isEditing">
							<option value="VND">VND</option>
							<option value="USD">USD</option>
							<option value="EUR">EUR</option>
						</select>
					</div>
					<div class="col-md-2">
						<label class="form-label">&nbsp;</label>
						<button class="btn btn-info w-100" @click="loadBalanceSheet" :disabled="isEditing">
							Tải dữ liệu
						</button>
					</div>
				</div>
			</div>

			<div class="toolbar mb-3 d-flex justify-content-between">
				<div>
					<template v-if="!isEditing">
						<button class="btn btn-primary me-2" @click="enableEdit">
							Chỉnh sửa
						</button>
						<button class="btn btn-danger" @click="deleteBalanceSheet">
							Xóa
						</button>
					</template>
					<template v-else>
						<button class="btn btn-success me-2" @click="saveChanges">
							Lưu
						</button>
						<button class="btn btn-secondary me-2" @click="cancelEdit">
							Hủy
						</button>
						<button class="btn btn-danger" @click="deleteBalanceSheet">
							Xóa
						</button>
					</template>
				</div>
				<div>
					<button class="btn btn-outline-primary btn-sm me-2" @click="showReportTypeManager = true">
						⚙️ Quản lý loại báo cáo
					</button>
					<button class="btn btn-outline-secondary btn-sm" @click="showCircularTemplateManager = true">
						⚙️ Quản lý mẫu thông tư
					</button>
				</div>
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
					<template v-for="sectionName in sectionNames" :key="sectionName">
						<tr class="section-header">
							<td colspan="5"><strong>{{ sectionLabels[sectionName] || sectionName }}</strong></td>
						</tr>
						
						<tr v-for="row in (sections[sectionName] || [])" :key="row.id" :class="{ 'indent-1': row.indent === 1, 'indent-2': row.indent === 2 }">
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
					</template>
				</tbody>
			</table>
		</div>

		<!-- Modal: Quản lý loại báo cáo -->
		<div v-if="showReportTypeManager" class="modal-overlay" @click.self="showReportTypeManager = false">
			<div class="modal-dialog modal-lg">
				<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title">Quản lý loại báo cáo</h5>
						<button type="button" class="btn-close" @click="showReportTypeManager = false"></button>
					</div>
					<div class="modal-body">
						<button class="btn btn-primary mb-3" @click="startAddReportType">+ Thêm mới</button>
						
						<table class="table table-bordered">
							<thead>
								<tr>
									<th>Tên báo cáo</th>
									<th>Mã</th>
									<th>Sections</th>
									<th>Trạng thái</th>
									<th>Thao tác</th>
								</tr>
							</thead>
							<tbody>
								<tr v-for="rt in reportTypesList" :key="rt.code">
									<td>{{ rt.report_name }}</td>
									<td><code>{{ rt.code }}</code></td>
									<td><small>{{ rt.sections_json }}</small></td>
									<td><span :class="rt.is_active ? 'badge bg-success' : 'badge bg-secondary'">{{ rt.is_active ? 'Kích hoạt' : 'Tắt' }}</span></td>
									<td>
										<button class="btn btn-sm btn-warning me-1" @click="startEditReportType(rt)">Sửa</button>
										<button class="btn btn-sm btn-danger" @click="deleteReportType(rt.name)">Xóa</button>
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>
			</div>
		</div>

		<!-- Modal: Quản lý mẫu thông tư -->
		<div v-if="showCircularTemplateManager" class="modal-overlay" @click.self="showCircularTemplateManager = false">
			<div class="modal-dialog modal-lg">
				<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title">Quản lý mẫu thông tư</h5>
						<button type="button" class="btn-close" @click="showCircularTemplateManager = false"></button>
					</div>
					<div class="modal-body">
						<button class="btn btn-primary mb-3" @click="startAddCircularTemplate">+ Thêm mới</button>
						
						<table class="table table-bordered">
							<thead>
								<tr>
									<th>Tên mẫu</th>
									<th>Mã</th>
									<th>Mô tả</th>
									<th>Trạng thái</th>
									<th>Thao tác</th>
								</tr>
							</thead>
							<tbody>
								<tr v-for="ct in circularTemplatesList" :key="ct.code">
									<td>{{ ct.template_name }}</td>
									<td><code>{{ ct.code }}</code></td>
									<td><small>{{ ct.description }}</small></td>
									<td><span :class="ct.is_active ? 'badge bg-success' : 'badge bg-secondary'">{{ ct.is_active ? 'Kích hoạt' : 'Tắt' }}</span></td>
									<td>
										<button class="btn btn-sm btn-warning me-1" @click="startEditCircularTemplate(ct)">Sửa</button>
										<button class="btn btn-sm btn-danger" @click="deleteCircularTemplate(ct.name)">Xóa</button>
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: 'BalanceSheet',
	emits: ['back'],
	data() {
		return {
			selectedCircularTemplate: '200',
			reportType: '',
			fiscalYear: '2025',
			currency: 'VND',
			isEditing: false,
			sections: {},
			backupData: null,
			loadedDocName: null,
			// Dynamic lists loaded from API
			reportTypesList: [],
			circularTemplatesList: [],
			// Manager modals
			showReportTypeManager: false,
			showCircularTemplateManager: false,
			// Form data for adding/editing
			editingReportType: null,
			editingCircularTemplate: null,
		};
	},
	computed: {
		reportTitle() {
			const rt = this.reportTypesList.find(r => r.code === this.reportType);
			return rt ? rt.report_name : 'Báo cáo tài chính';
		},
		filteredReportTypes() {
			console.log('=== filteredReportTypes ===');
			console.log('selectedCircularTemplate:', this.selectedCircularTemplate, typeof this.selectedCircularTemplate);
			console.log('reportTypesList:', this.reportTypesList);
			
			// Ensure string comparison (DB might return string or number)
			const filtered = this.reportTypesList.filter(rt => {
				const match = String(rt.circular_template) === String(this.selectedCircularTemplate);
				console.log(`Compare: rt.circular_template=${rt.circular_template} (${typeof rt.circular_template}) vs selected=${this.selectedCircularTemplate} (${typeof this.selectedCircularTemplate}) => ${match}`);
				return match;
			});
			console.log('filtered:', filtered);
			return filtered;
		},
		sectionNames() {
			const rt = this.reportTypesList.find(r => r.code === this.reportType);
			if (!rt || !rt.sections_json) return [];
			
			try {
				const sections = JSON.parse(rt.sections_json);
				return Array.isArray(sections) ? sections : [];
			} catch (e) {
				console.error('Error parsing sections_json:', e);
				return [];
			}
		},
		sectionLabels() {
			const labels = {
				Asset: 'Tài sản',
				Equity: 'Nguồn vốn',
				Revenue: 'Doanh thu',
				Expense: 'Chi phí',
				Other: 'Khác',
				Operating: 'Hoạt động kinh doanh',
				Investing: 'Hoạt động đầu tư',
				Financing: 'Hoạt động tài chính',
			};
			return labels;
		},
	},
	async created() {
		await this.loadDropdownOptions();
		this.resetTableToDefault();
	},
	methods: {
		async loadDropdownOptions() {
			try {
				const csrfToken = window.getCSRFToken ? window.getCSRFToken() : (window.csrf_token || '');
				
				// Load Report Types
				const rtResponse = await fetch('/api/method/custom_app.customdemo.doctype.balance_sheet.balance_sheet.get_report_types', {
					method: 'GET',
					headers: {
						'Content-Type': 'application/json',
						'X-Frappe-CSRF-Token': csrfToken,
					},
					credentials: 'include',
				});
				const rtResult = await rtResponse.json();
				if (rtResult.message && rtResult.message.success) {
					this.reportTypesList = rtResult.message.data;
					// Set default report type based on selected circular template
					if (this.reportTypesList.length > 0 && !this.reportType) {
						const filtered = this.reportTypesList.filter(rt => rt.circular_template === this.selectedCircularTemplate);
						if (filtered.length > 0) {
							this.reportType = filtered[0].code;
						}
					}
				}
				
				// Load Circular Templates
				// Load Circular Templates (for manager modal only)
				const ctResponse = await fetch('/api/method/custom_app.customdemo.doctype.balance_sheet.balance_sheet.get_circular_templates', {
					method: 'GET',
					headers: {
						'Content-Type': 'application/json',
						'X-Frappe-CSRF-Token': csrfToken,
					},
					credentials: 'include',
				});
				const ctResult = await ctResponse.json();
				if (ctResult.message && ctResult.message.success) {
					this.circularTemplatesList = ctResult.message.data;
				}
			} catch (err) {
				console.error('Error loading dropdown options:', err);
				// Fallback to hardcoded values if API fails
			}
		},
		getDefaultRowsForSection(sectionName) {
			// Default templates cho từng section (có thể mở rộng sau)
			const templates = {
				Asset: [
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
				Equity: [
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
				Revenue: [
					{ id: 'r1', label: 'Doanh thu bán hàng và cung cấp dịch vụ', code: '01', note: '', startYear: 0, endYear: 0, indent: 0, parentId: null },
					{ id: 'r2', label: 'Các khoản giảm trừ doanh thu', code: '02', note: '', startYear: 0, endYear: 0, indent: 0, parentId: null },
					{ id: 'r3', label: 'Doanh thu thuần về bán hàng và cung cấp dịch vụ', code: '10', note: '', startYear: 0, endYear: 0, indent: 0, parentId: null },
				],
				Expense: [
					{ id: 'e1', label: 'Giá vốn hàng bán', code: '11', note: '', startYear: 0, endYear: 0, indent: 0, parentId: null },
					{ id: 'e2', label: 'Chi phí bán hàng', code: '20', note: '', startYear: 0, endYear: 0, indent: 0, parentId: null },
					{ id: 'e3', label: 'Chi phí quản lý doanh nghiệp', code: '21', note: '', startYear: 0, endYear: 0, indent: 0, parentId: null },
				],
				Other: [
					{ id: 'o1', label: 'Thu nhập khác', code: '40', note: '', startYear: 0, endYear: 0, indent: 0, parentId: null },
					{ id: 'o2', label: 'Chi phí khác', code: '41', note: '', startYear: 0, endYear: 0, indent: 0, parentId: null },
				],
				Operating: [
					{ id: 'op1', label: 'Lưu chuyển tiền từ hoạt động kinh doanh', code: 'I', note: '', startYear: 0, endYear: 0, indent: 0, parentId: null },
				],
				Investing: [
					{ id: 'inv1', label: 'Lưu chuyển tiền từ hoạt động đầu tư', code: 'II', note: '', startYear: 0, endYear: 0, indent: 0, parentId: null },
				],
				Financing: [
					{ id: 'fin1', label: 'Lưu chuyển tiền từ hoạt động tài chính', code: 'III', note: '', startYear: 0, endYear: 0, indent: 0, parentId: null },
				],
			};
			return templates[sectionName] || [];
		},
		onCircularTemplateChange() {
			if (this.isEditing) return;
			// Auto-select first report type of the new circular template
			const filtered = this.reportTypesList.filter(rt => rt.circular_template === this.selectedCircularTemplate);
			if (filtered.length > 0) {
				this.reportType = filtered[0].code;
			} else {
				this.reportType = '';
			}
			this.resetTableToDefault();
		},
		onReportTypeChange() {
			if (this.isEditing) return;
			this.resetTableToDefault();
		},
		resetTableToDefault() {
			this.loadedDocName = null;
			const newSections = {};
			for (const sectionName of this.sectionNames) {
				newSections[sectionName] = this.getDefaultRowsForSection(sectionName);
			}
			this.sections = newSections;
		},
		async loadBalanceSheet() {
			try {
				const csrfToken = window.getCSRFToken ? window.getCSRFToken() : (window.csrf_token || '');
				const response = await fetch(
					`/api/method/custom_app.customdemo.doctype.balance_sheet.balance_sheet.get_balance_sheet_by_filters?report_type=${this.reportType}&fiscal_year=${this.fiscalYear}`,
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
					this.loadedDocName = data?.name || null;
					const parsedData = data?.parsed_data;
					
					// parsedData.sections: { SectionName: [...rows] }
					const loadedSections = parsedData?.sections;
					if (!loadedSections || Object.keys(loadedSections).length === 0) {
						this.resetTableToDefault();
						await this.$nextTick();
						alert('Không có dữ liệu cho loại báo cáo/năm/mẫu đã chọn. Bảng đã được reset về 0.');
						return;
					}
					
					// Load sections
					const newSections = {};
					for (const sectionName of this.sectionNames) {
						if (loadedSections[sectionName] && Array.isArray(loadedSections[sectionName])) {
							newSections[sectionName] = loadedSections[sectionName];
						} else {
							newSections[sectionName] = this.getDefaultRowsForSection(sectionName);
						}
					}
					this.sections = newSections;
					await this.$nextTick();
					alert(`Đã tải dữ liệu: ${data.title}`);
				} else {
					this.loadedDocName = null;
					this.resetTableToDefault();
					await this.$nextTick();
					alert(result.message?.message || 'Không tìm thấy dữ liệu. Bảng đã được reset về 0.');
				}
			} catch (err) {
				console.error('Error loading balance sheet:', err);
				alert('Lỗi khi tải dữ liệu. Vui lòng xem Console.');
			}
		},
		async deleteBalanceSheet() {
			const ok = window.confirm(
				`Bạn có chắc muốn XÓA dữ liệu "${this.reportTitle}" cho:\n\n- Năm tài chính: ${this.fiscalYear}\n\nThao tác này sẽ xóa dữ liệu trong DB và reset bảng về mặc định (0).`
			);
			if (!ok) return;

			try {
				const csrfToken = window.getCSRFToken ? window.getCSRFToken() : (window.csrf_token || '');
				const payload = this.loadedDocName
					? { name: this.loadedDocName }
					: { report_type: this.reportType, fiscal_year: this.fiscalYear };

				const response = await fetch(
					'/api/method/custom_app.customdemo.doctype.balance_sheet.balance_sheet.delete_balance_sheet',
					{
						method: 'POST',
						headers: {
							'Content-Type': 'application/json',
							'X-Frappe-CSRF-Token': csrfToken,
						},
						credentials: 'include',
						body: JSON.stringify(payload),
					}
				);
				const result = await response.json();

				if (!(response.ok && result.message && result.message.success)) {
					console.error('Delete Balance Sheet failed:', result);
					alert('Xóa thất bại. Vui lòng xem Console/Network.');
					return;
				}

				// Reset UI state
				this.isEditing = false;
				this.backupData = null;
				this.resetTableToDefault();
				await this.$nextTick();
				alert(`Đã xóa thành công (${result.message.deleted || 0} bản ghi). Bảng đã được reset về 0.`);
			} catch (err) {
				console.error('Error calling delete_balance_sheet API:', err);
				alert('Gọi API xóa bị lỗi. Vui lòng xem Console.');
			}
		},
		enableEdit() {
			this.isEditing = true;
			this.backupData = JSON.parse(JSON.stringify(this.sections));
		},
		async saveChanges() {
			// Nếu không thay đổi gì so với lúc bấm "Chỉnh sửa" thì hỏi xác nhận trước khi lưu
			try {
				if (this.backupData) {
					const isUnchanged = JSON.stringify(this.sections) === JSON.stringify(this.backupData);

					// Nếu vẫn y nguyên, hoặc toàn bộ số đều = 0 -> confirm
					const allNumbersAreZero = (sections) => {
						for (const rows of Object.values(sections)) {
							if (!Array.isArray(rows)) continue;
							for (const r of rows) {
								const start = Number(r?.startYear ?? 0);
								const end = Number(r?.endYear ?? 0);
								if (start !== 0 || end !== 0) return false;
							}
						}
						return true;
					};

					const isAllZero = allNumbersAreZero(this.sections);

					if (isUnchanged || isAllZero) {
						const ok = window.confirm(
							isUnchanged
								? 'Bạn chưa thay đổi dữ liệu nào. Vẫn muốn lưu không?'
								: 'Tất cả số liệu hiện đang bằng 0. Vẫn muốn lưu không?'
						);
						if (!ok) {
							return;
						}
					}
				}
			} catch (e) {
				// Nếu có lỗi khi so sánh, bỏ qua và vẫn cho phép lưu
			}

			// Chuyển data thành JSON
			const jsonData = {
				title: `${this.reportTitle} ${this.fiscalYear}`,
				report_type: this.reportType,
				fiscal_year: this.fiscalYear,
				currency: this.currency,
				timestamp: new Date().toISOString(),
				data: {
					sections: this.sections,
				}
			};

			// Console log để debug
			console.log('=== SAVE BALANCE SHEET DATA ===');
			console.log('Report Type:', this.reportType);
			console.log('Fiscal Year:', this.fiscalYear);
			console.log('Full JSON Data:', JSON.stringify(jsonData, null, 2));

			// Gửi data JSON lên API Frappe để backend lưu DB
			try {
				const csrfToken = window.getCSRFToken ? window.getCSRFToken() : (window.csrf_token || '');
				const response = await fetch('/api/method/custom_app.customdemo.doctype.balance_sheet.balance_sheet.save_balance_sheet', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'X-Frappe-CSRF-Token': csrfToken,
					},
					credentials: 'include',
					body: JSON.stringify({
						payload: JSON.stringify(jsonData),
						// If a document was loaded, send its name so backend overwrites it
						name: this.loadedDocName,
					}),
				});
				const data = await response.json();
				if (!(response.ok && data.message && data.message.success)) {
					console.error('Save Balance Sheet failed:', data);
					alert('Lưu thất bại. Vui lòng xem Console/Network.');
				} else {
					// thành công -> trả docname để tiện trace
					alert(`Đã lưu thành công!\n\nDocname: ${data.message.name}`);
				}
			} catch (err) {
				console.error('Error calling save_balance_sheet API:', err);
				alert('Gọi API lưu bị lỗi. Vui lòng xem Console/Network.');
			}

			// Tắt chế độ edit
			this.isEditing = false;
			this.backupData = null;

			// Tùy chọn: Lưu vào localStorage
			localStorage.setItem('balanceSheetData', JSON.stringify(jsonData));
		},
		cancelEdit() {
			if (this.backupData) {
				this.sections = JSON.parse(JSON.stringify(this.backupData));
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

/* Modal styles */
.modal-overlay {
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	background: rgba(0, 0, 0, 0.5);
	display: flex;
	justify-content: center;
	align-items: center;
	z-index: 9999;
}
.modal-dialog {
	background: white;
	border-radius: 8px;
	max-width: 800px;
	width: 90%;
	max-height: 80vh;
	overflow-y: auto;
}
.modal-content {
	padding: 0;
}
.modal-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 1rem;
	border-bottom: 1px solid #dee2e6;
}
.modal-body {
	padding: 1rem;
}
.btn-close {
	background: transparent;
	border: none;
	font-size: 1.5rem;
	cursor: pointer;
}
