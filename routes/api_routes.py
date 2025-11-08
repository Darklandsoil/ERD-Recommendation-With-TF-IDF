from flask import Blueprint
from controllers.erd_controller import ERDController

api_bp = Blueprint('api', __name__, url_prefix='/api')

# ERD search and management routes
api_bp.add_url_rule('/search-erd', 'search_erd', ERDController.search_erd, methods=['POST'])
api_bp.add_url_rule('/list-erds', 'list_erds', ERDController.list_erds, methods=['GET'])
api_bp.add_url_rule('/reload-system', 'reload_system', ERDController.reload_system, methods=['POST'])

# Advisor ERD routes
api_bp.add_url_rule('/add-erd', 'add_erd', ERDController.add_erd, methods=['POST'])  # Create ERD (legacy path)
api_bp.add_url_rule('/advisor-erds', 'advisor_erds', ERDController.get_advisor_erds, methods=['GET'])  # Get advisor's ERDs (legacy path)
api_bp.add_url_rule('/erd/<erd_id>', 'get_erd_detail', ERDController.get_erd_detail, methods=['GET'])  # Get ERD detail
api_bp.add_url_rule('/erd/<erd_id>', 'update_erd', ERDController.update_erd, methods=['PUT'])  # Update ERD
api_bp.add_url_rule('/erd/<erd_id>', 'delete_erd_by_id', ERDController.delete_erd_by_id, methods=['DELETE'])  # Delete ERD

# Alternative modern paths
api_bp.add_url_rule('/erds', 'create_erd', ERDController.add_erd, methods=['POST'])  # Create ERD
api_bp.add_url_rule('/erds/my-erds', 'my_erds', ERDController.get_advisor_erds, methods=['GET'])  # Get advisor's ERDs

# Legacy delete endpoint (by name)
api_bp.add_url_rule('/delete-erd', 'delete_erd', ERDController.delete_erd, methods=['DELETE'])

# ERD generation and download routes
api_bp.add_url_rule('/generate-erd-image/<erd_name>', 'generate_erd_image', ERDController.generate_erd_image, methods=['GET'])
api_bp.add_url_rule('/download-erd/<filename>', 'download_erd', ERDController.download_erd, methods=['GET'])