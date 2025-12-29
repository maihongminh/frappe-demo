import { createApp } from 'vue';
import App from './App.vue';

console.log('[custom_app] main.js loaded');

// Ensure jQuery global exists for legacy frappe/website scripts
if (typeof window !== 'undefined') {
	const jq = window.$ || window.jQuery || (window.frappe && window.frappe.$);
	if (jq) {
		window.$ = jq;
		window.jQuery = jq;
		console.log('[custom_app] jQuery detected, $ wired');
	} else {
		console.warn('[custom_app] jQuery not found on window/frappe');
	}

	// Helper function: Get CSRF token from multiple sources
	window.getCSRFToken = function() {
		// 1) Try window.frappe.csrf_token (standard Frappe)
		if (window.frappe && window.frappe.csrf_token) {
			return window.frappe.csrf_token;
		}
		// 2) Try window.csrf_token (legacy/fallback)
		if (window.csrf_token) {
			return window.csrf_token;
		}
		// 3) Try reading from cookie 'csrf_token'
		const cookies = document.cookie.split(';');
		for (let cookie of cookies) {
			const [key, value] = cookie.trim().split('=');
			if (key === 'csrf_token') {
				return decodeURIComponent(value);
			}
		}
		console.warn('[custom_app] CSRF token not found!');
		return '';
	};
	console.log('[custom_app] getCSRFToken helper registered');
}

const app = createApp(App);
let mounted = false;

function mountVueApp(source = 'unknown') {
	if (mounted) return;
	const mountPoint = document.getElementById('vue-app');
	if (!mountPoint) {
		console.warn('[custom_app] #vue-app element not found when mounting from', source);
		return;
	}
	console.log('[custom_app] Mounting Vue app from', source);
		app.mount('#vue-app');
	mounted = true;
}

// 1) Try via frappe.ready (if không bị lỗi jQuery chặn)
if (typeof frappe !== 'undefined' && typeof frappe.ready === 'function') {
	console.log('[custom_app] frappe.ready available, registering mount callback');
	try {
		frappe.ready(() => {
			console.log('[custom_app] frappe.ready callback fired');
			mountVueApp('frappe.ready');
		});
	} catch (e) {
		console.error('[custom_app] Error in frappe.ready hook', e);
	}
} else {
	console.warn('[custom_app] frappe.ready is not available');
}

// 2) Fallback: DOMContentLoaded (không phụ thuộc jQuery / frappe.ready)
if (document.readyState === 'loading') {
	window.addEventListener('DOMContentLoaded', () => {
		console.log('[custom_app] DOMContentLoaded fallback');
		mountVueApp('DOMContentLoaded');
	});
} else {
	// DOM đã sẵn sàng
	console.log('[custom_app] document already ready, mounting immediately');
	mountVueApp('immediate');
}

