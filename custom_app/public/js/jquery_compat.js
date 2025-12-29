// Ensure global $ / jQuery exist for legacy frappe website scripts
(function () {
	if (typeof window === 'undefined') return;
	// Prefer existing jQuery from frappe or global
	var jq = window.jQuery || (window.frappe && window.frappe.jQuery) || window.$;
	if (!jq) return;
	window.jQuery = jq;
	window.$ = jq;
})();

