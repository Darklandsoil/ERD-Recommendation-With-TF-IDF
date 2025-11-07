from flask import Blueprint, render_template
from controllers.admin_controller import AdminController

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin page route
@admin_bp.route('/dashboard')
def admin_dashboard():
    """Admin dashboard page"""
    return render_template('admin_dashboard.html')

# Admin API routes - Advisor Management
admin_bp.add_url_rule('/api/advisors', 'get_advisors', AdminController.get_all_advisors, methods=['GET'])
admin_bp.add_url_rule('/api/advisors/create', 'create_advisor', AdminController.create_advisor, methods=['POST'])
admin_bp.add_url_rule('/api/advisors/update', 'update_advisor', AdminController.update_advisor, methods=['PUT'])
admin_bp.add_url_rule('/api/advisors/delete', 'delete_advisor', AdminController.delete_advisor, methods=['DELETE'])

# Admin API routes - Statistics & Monitoring
admin_bp.add_url_rule('/api/statistics', 'get_statistics', AdminController.get_statistics, methods=['GET'])
admin_bp.add_url_rule('/api/advisor-monitoring', 'get_advisor_monitoring', AdminController.get_advisor_monitoring, methods=['GET'])
