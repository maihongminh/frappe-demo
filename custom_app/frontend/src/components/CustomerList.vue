<template>
	<div class="container mt-5">
		<div class="row">
			<div class="col-12">
				<nav aria-label="breadcrumb">
					<ol class="breadcrumb">
						<li class="breadcrumb-item"><a href="/">Home</a></li>
						<li class="breadcrumb-item active" aria-current="page">Customers</li>
					</ol>
				</nav>

				<h1 class="mb-4">Customers</h1>

				<div class="row">
					<div class="col-md-5 mb-4">
						<div class="card">
							<div class="card-body">
								<h5 class="card-title">Add Customer</h5>
								<form @submit.prevent="handleSubmit">
									<div class="form-group mb-3">
										<label for="customer_name">Name <span class="text-danger">*</span></label>
										<input
											v-model.trim="form.customer_name"
											type="text"
											class="form-control"
											id="customer_name"
											required
										/>
									</div>

									<div class="form-group mb-3">
										<label for="email">Email</label>
										<input
											v-model.trim="form.email"
											type="email"
											class="form-control"
											id="email"
										/>
									</div>

									<div class="form-group mb-3">
										<label for="phone">Phone</label>
										<input
											v-model.trim="form.phone"
											type="text"
											class="form-control"
											id="phone"
										/>
									</div>

									<div class="form-group mb-3">
										<label for="role">Role</label>
										<select v-model="form.role" class="form-control" id="role">
											<option value="">-- Select --</option>
											<option value="Customer">Customer</option>
											<option value="VIP">VIP</option>
											<option value="Partner">Partner</option>
										</select>
									</div>

									<div class="form-group mb-3">
										<label for="address">Address</label>
										<textarea
											v-model.trim="form.address"
											class="form-control"
											id="address"
											rows="3"
										></textarea>
									</div>

									<button type="submit" class="btn btn-primary">Save</button>
									<button type="button" class="btn btn-secondary ml-2" @click="$emit('back')">
										Back to Home
									</button>

									<div
										v-if="formMessage.message"
										class="mt-3 alert"
										:class="formMessage.type === 'success' ? 'alert-success' : 'alert-danger'"
									>
										{{ formMessage.message }}
									</div>
								</form>
							</div>
						</div>
					</div>

					<div class="col-md-7 mb-4">
						<div class="card">
							<div class="card-body">
								<h5 class="card-title d-flex justify-content-between align-items-center">
									<span>Customer List</span>
								</h5>

								<div class="row mb-3">
									<div class="col-md-7">
										<input
											v-model.trim="filterSearch"
											type="text"
											class="form-control form-control-sm"
											placeholder="Search by name, email, phone, address..."
										/>
									</div>
									<div class="col-md-5 mt-2 mt-md-0">
										<select v-model="filterRole" class="form-control form-control-sm">
											<option value="">All roles</option>
											<option value="Customer">Customer</option>
											<option value="VIP">VIP</option>
											<option value="Partner">Partner</option>
										</select>
									</div>
								</div>

								<div class="table-responsive">
									<table class="table table-striped">
										<thead>
											<tr>
												<th>Name</th>
												<th>Email</th>
												<th>Phone</th>
												<th>Role</th>
												<th>Address</th>
												<th class="actions-header">Actions</th>
											</tr>
										</thead>
										<tbody>
											<tr v-if="loading">
												<td colspan="6" class="text-muted text-center">Loading...</td>
											</tr>
											<tr v-else-if="filteredCustomers.length === 0">
												<td colspan="6" class="text-muted text-center">No customers yet.</td>
											</tr>
											<tr v-else v-for="customer in filteredCustomers" :key="customer.name">
												<td>{{ customer.customer_name || '' }}</td>
												<td>{{ customer.email || '' }}</td>
												<td>{{ customer.phone || '' }}</td>
												<td>{{ customer.role || '' }}</td>
												<td class="address-cell">{{ customer.address || '' }}</td>
												<td class="actions-cell">
													<button
														type="button"
														class="btn btn-sm btn-outline-primary btn-edit"
														@click="handleEdit(customer.name)"
													>
														Edit
													</button>
													<button
														type="button"
														class="btn btn-sm btn-outline-danger btn-delete ml-1"
														@click="handleDelete(customer.name)"
													>
														Delete
													</button>
												</td>
											</tr>
										</tbody>
									</table>
									<div
										v-if="listMessage"
										class="mt-2 alert"
										:class="listMessageType === 'success' ? 'alert-success' : listMessageType === 'danger' ? 'alert-danger' : 'alert-info'"
									>
										{{ listMessage }}
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: 'CustomerList',
	data() {
		return {
			form: {
				customer_name: '',
				email: '',
				phone: '',
				role: '',
				address: '',
			},
			formMessage: {
				message: '',
				type: 'success',
			},
			allCustomers: [],
			loading: true,
			filterSearch: '',
			filterRole: '',
			listMessage: '',
			listMessageType: 'info',
		};
	},
	computed: {
		filteredCustomers() {
			let filtered = this.allCustomers.slice();

			const keyword = this.filterSearch.toLowerCase().trim();
			const role = this.filterRole.trim();

			if (keyword) {
				filtered = filtered.filter((c) => {
					const values = [
						c.customer_name,
						c.email,
						c.phone,
						c.address,
					].map((v) => (v || '').toLowerCase());

					return values.some((v) => v.includes(keyword));
				});
			}

			if (role) {
				filtered = filtered.filter((c) => (c.role || '') === role);
			}

			return filtered;
		},
	},
	mounted() {
		this.loadCustomers();
	},
	watch: {
		filterSearch() {
			// Filter is computed, no need to do anything
		},
		filterRole() {
			// Filter is computed, no need to do anything
		},
	},
	methods: {
		resetFormMessage() {
			this.formMessage.message = '';
		},
		showFormMessage(message, type = 'success') {
			this.formMessage.message = message;
			this.formMessage.type = type;
		},
		showListMessage(message, type = 'info') {
			this.listMessage = message;
			this.listMessageType = type;
		},
		async loadCustomers() {
			this.loading = true;
			try {
				const response = await fetch('/api/method/custom_app.customdemo.doctype.customer.customer.get_customers', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'X-Frappe-CSRF-Token': window.csrf_token || '',
					},
				});

				const data = await response.json();

				if (response.ok && data.message) {
					this.allCustomers = data.message || [];
				}
			} catch (err) {
				console.error('Error loading customers:', err);
				this.showListMessage('Error loading customers.', 'danger');
			} finally {
				this.loading = false;
			}
		},
		async handleSubmit() {
			this.resetFormMessage();

			const customer_name = this.form.customer_name.trim();
			if (!customer_name) {
				this.showFormMessage('Name is required.', 'danger');
				return;
			}

			const payload = {
				customer_name,
				email: this.form.email.trim(),
				phone: this.form.phone.trim(),
				role: this.form.role,
				address: this.form.address.trim(),
			};

			this.showFormMessage('Saving...', 'info');

			try {
				const response = await fetch('/api/method/custom_app.customdemo.doctype.customer.customer.create_customer', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'X-Frappe-CSRF-Token': window.csrf_token || '',
					},
					body: JSON.stringify(payload),
				});

				const data = await response.json();

				if (response.ok && data.message && data.message.success) {
					this.showFormMessage('Saved successfully!', 'success');
					this.form.customer_name = '';
					this.form.email = '';
					this.form.phone = '';
					this.form.role = '';
					this.form.address = '';
					this.loadCustomers();
				} else {
					this.showFormMessage('Error saving customer.', 'danger');
				}
			} catch (err) {
				console.error('Error saving customer:', err);
				this.showFormMessage('Error saving customer.', 'danger');
			}
		},
		handleEdit(name) {
			if (!name) return;
			window.location.href = '/feature1_edit?name=' + encodeURIComponent(name);
		},
		async handleDelete(name) {
			if (!name) return;

			if (!confirm('Bạn có chắc chắn muốn xóa customer này không?')) {
				return;
			}

			this.showListMessage('Deleting...', 'info');

			try {
				const response = await fetch('/api/method/custom_app.customdemo.doctype.customer.customer.delete_customer', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'X-Frappe-CSRF-Token': window.csrf_token || '',
					},
					body: JSON.stringify({ name }),
				});

				const data = await response.json();

				if (response.ok && data.message && data.message.success) {
					this.showListMessage('Deleted successfully.', 'success');
					this.loadCustomers();
				} else {
					this.showListMessage('Failed to delete customer.', 'danger');
				}
			} catch (err) {
				console.error('Error deleting customer:', err);
				this.showListMessage('Error while deleting customer.', 'danger');
			}
		},
	},
};
</script>

<style scoped>
.card {
	border: none;
	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card-title {
	margin-bottom: 1rem;
}

.table {
	width: 100%;
	table-layout: auto;
}

.table th,
.table td {
	vertical-align: middle;
	white-space: nowrap;
}

.address-cell {
	max-width: 160px;
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
}

.actions-header {
	width: 1%;
	white-space: nowrap;
}

.actions-cell {
	white-space: nowrap;
}
</style>

