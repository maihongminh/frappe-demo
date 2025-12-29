import frappe

def get_context(context):
	context.no_cache = 1
	context.show_sidebar = False
	# Inject CSRF token for API calls
	context.csrf_token = frappe.sessions.get_csrf_token()
	return context
