<template>
	<div>
		<section v-if="currentView === 'home'" class="hero-section text-center">
			<div class="container">
				<h1 class="display-4 mb-3">Welcome to CustomDemo</h1>
				<p class="lead">Vue 3 demo with navigation to Customer management.</p>
			</div>
		</section>

		<div v-if="currentView === 'home'" class="container mt-5">
			<div class="row">
				<div class="col-md-4 mb-4">
					<button
						type="button"
						class="card card-clickable h-100 w-100 text-start"
						@click="go('/feature1')"
					>
						<div class="card-body">
							<h5 class="card-title">Doctype new customer</h5>
							<p class="card-text">create a new customer.</p>
							<span class="btn btn-link p-0">Mở form</span>
						</div>
					</button>
				</div>
				<div class="col-md-4 mb-4">
					<button
						type="button"
						class="card card-clickable h-100 w-100 text-start"
						@click="go('/feature2')"
					>
						<div class="card-body">
							<h5 class="card-title">Bảng cân đối kế toán</h5>
							<p class="card-text">Quản lý tài sản và nguồn vốn.</p>
							<span class="btn btn-link p-0">Xem bảng cân đối</span>
						</div>
					</button>
				</div>
				<div class="col-md-4 mb-4">
					<button
						type="button"
						class="card card-clickable h-100 w-100 text-start"
						@click="go('/feature3')"
					>
						<div class="card-body">
							<h5 class="card-title">Feature 3</h5>
							<p class="card-text">Description.</p>
							<span class="btn btn-link p-0">Xem trang</span>
						</div>
					</button>
				</div>
			</div>
		</div>

		<CustomerList
			v-else-if="currentView === 'customer_list'"
			@back="handleBack"
		/>

		<CustomerEdit
			v-else-if="currentView === 'customer_edit'"
			:customer-name="editCustomerName"
			@back="handleBack"
		/>

		<BalanceSheet
			v-else-if="currentView === 'balance_sheet'"
			@back="handleBack"
		/>
	</div>
</template>

<script>
import CustomerList from './components/CustomerList.vue';
import CustomerEdit from './components/CustomerEdit.vue';
import BalanceSheet from './components/BalanceSheet.vue';

export default {
	name: 'App',
	components: {
		CustomerList,
		CustomerEdit,
		BalanceSheet,
	},
	data() {
		return {
			currentView: 'home',
			editCustomerName: null,
		};
	},
	mounted() {
		this.initializeView();
	},
	methods: {
		initializeView() {
			if (typeof window !== 'undefined') {
				const path = window.location.pathname || '';
				const params = new URLSearchParams(window.location.search);
				
				if (path.startsWith('/feature1_edit')) {
					const name = params.get('name');
					if (name) {
						this.editCustomerName = name;
						this.currentView = 'customer_edit';
						return;
					}
				}
				
				if (path.startsWith('/feature1')) {
					this.currentView = 'customer_list';
					return;
			}

			if (path.startsWith('/feature2')) {
				this.currentView = 'balance_sheet';
				return;
			}
				
				// Home page or vue_demo page
				if (path === '/' || path === '/index' || path.startsWith('/vue_demo')) {
					this.currentView = 'home';
					return;
				}
			}
			this.currentView = 'home';
		},
		go(href) {
			// Remember where the user came from so "Back" can return to the same home route
			// (in this app, home can be served at `/`, `/index`, or `/vue_demo`).
			if (typeof window !== 'undefined') {
				const current = `${window.location.pathname || ''}${window.location.search || ''}`;
				const isGoingToFeature = href.startsWith('/feature');
				const isCurrentlyHome =
					window.location.pathname === '/' ||
					window.location.pathname === '/index' ||
					(window.location.pathname || '').startsWith('/vue_demo');

				// Only overwrite return target when leaving home for a feature.
				if (isGoingToFeature && isCurrentlyHome) {
					sessionStorage.setItem('vue_demo:return_to', current || '/vue_demo');
				}
			}
			window.location.href = href;
		},
		handleBack() {
			if (typeof window !== 'undefined') {
				const path = window.location.pathname || '';
				const returnTo = sessionStorage.getItem('vue_demo:return_to');

				if (path.startsWith('/feature1') || path.startsWith('/feature1_edit') || path.startsWith('/feature2')) {
					this.go(returnTo || '/vue_demo');
					return;
				}
			}
			this.currentView = 'home';
		},
	},
};
</script>

<style scoped>
.hero-section {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	color: #fff;
	padding: 72px 0;
}

.card {
	border: none;
	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.card-clickable {
	cursor: pointer;
	color: inherit;
}

.card-clickable:hover {
	transform: translateY(-4px);
	box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.card-clickable:hover .card-title {
	color: #667eea;
}
</style>

