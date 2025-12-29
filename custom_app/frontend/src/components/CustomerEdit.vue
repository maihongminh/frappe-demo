<template>
	<div class="container mt-5">
		<div class="row">
			<div class="col-12">
				<nav aria-label="breadcrumb">
					<ol class="breadcrumb">
						<li class="breadcrumb-item"><a href="/">Home</a></li>
						<li class="breadcrumb-item"><a href="/feature1">Customers</a></li>
						<li class="breadcrumb-item active" aria-current="page">Edit Customer</li>
					</ol>
				</nav>

				<h1 class="mb-4">Edit Customer</h1>

				<div class="row">
					<div class="col-md-6 mb-4">
						<div class="card">
							<div class="card-body">
								<h5 class="card-title">Customer Information</h5>
								<form @submit.prevent="handleSubmit">
									<input type="hidden" :value="customerName" />

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

									<button type="submit" class="btn btn-primary" :disabled="submitting">
										<span v-if="submitting">Updating...</span>
										<span v-else>Update</span>
									</button>
									<button type="button" class="btn btn-secondary ml-2" @click="$emit('back')">
										Back to Customer List
									</button>

									<div
										v-if="message"
										class="mt-3 alert"
										:class="messageType === 'success' ? 'alert-success' : messageType === 'danger' ? 'alert-danger' : 'alert-info'"
									>
										{{ message }}
									</div>
								</form>
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
	name: 'CustomerEdit',
	props: {
		customerName: {
			type: String,
			required: true,
		},
	},
	data() {
		return {
			form: {
				customer_name: '',
				email: '',
				phone: '',
				role: '',
				address: '',
			},
			message: '',
			messageType: 'info',
			submitting: false,
			loading: true,
		};
	},
	mounted() {
		if (!this.customerName) {
			this.message = 'Customer not found.';
			this.messageType = 'danger';
			setTimeout(() => {
				window.location.href = '/feature1';
			}, 2000);
			return;
		}

		this.loadCustomer();
	},
	methods: {
		async loadCustomer() {
			this.message = 'Loading customer...';
			this.messageType = 'info';
			this.loading = true;

			try {
				const csrfToken = window.getCSRFToken ? window.getCSRFToken() : (window.csrf_token || '');
				const response = await fetch('/api/method/custom_app.customdemo.doctype.customer.customer.get_customer', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'X-Frappe-CSRF-Token': csrfToken,
					},
					credentials: 'include',
					body: JSON.stringify({ name: this.customerName }),
				});

				const data = await response.json();

				if (!response.ok || !data.message) {
					this.message = 'Customer not found.';
					this.messageType = 'danger';
					return;
				}

				const c = data.message;
				this.form.customer_name = c.customer_name || '';
				this.form.email = c.email || '';
				this.form.phone = c.phone || '';
				this.form.role = c.role || '';
				this.form.address = c.address || '';

				this.message = '';
			} catch (err) {
				console.error('Error loading customer:', err);
				this.message = 'Error loading customer.';
				this.messageType = 'danger';
			} finally {
				this.loading = false;
			}
		},
		async handleSubmit() {
			this.message = '';

			const customer_name = this.form.customer_name.trim();
			if (!customer_name) {
				this.message = 'Name is required.';
				this.messageType = 'danger';
				return;
			}

			const payload = {
				name: this.customerName,
				customer_name,
				email: this.form.email.trim(),
				phone: this.form.phone.trim(),
				role: this.form.role,
				address: this.form.address.trim(),
			};

			this.message = 'Updating...';
			this.messageType = 'info';
			this.submitting = true;

			try {
				const csrfToken = window.getCSRFToken ? window.getCSRFToken() : (window.csrf_token || '');
				const response = await fetch('/api/method/custom_app.customdemo.doctype.customer.customer.update_customer', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'X-Frappe-CSRF-Token': csrfToken,
					},
					credentials: 'include',
					body: JSON.stringify(payload),
				});

				const data = await response.json();

				if (response.ok && data.message && data.message.success) {
					this.message = 'Updated successfully! Redirecting...';
					this.messageType = 'success';
					setTimeout(() => {
						window.location.href = '/feature1';
					}, 1000);
				} else {
					this.message = 'Error updating customer.';
					this.messageType = 'danger';
				}
			} catch (err) {
				console.error('Error updating customer:', err);
				this.message = 'Error updating customer.';
				this.messageType = 'danger';
			} finally {
				this.submitting = false;
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
</style>

