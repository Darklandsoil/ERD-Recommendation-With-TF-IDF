from flask import Blueprint
from controllers.erd_controller import ERDController

api_bp = Blueprint('api', __name__, url_prefix='/api')

# ERD search and management routes
api_bp.add_url_rule('/search-erd', 'search_erd', ERDController.search_erd, methods=['POST'])
api_bp.add_url_rule('/add-erd', 'add_erd', ERDController.add_erd, methods=['POST'])
api_bp.add_url_rule('/delete-erd', 'delete_erd', ERDController.delete_erd, methods=['DELETE'])
api_bp.add_url_rule('/advisor-erds', 'advisor_erds', ERDController.get_advisor_erds, methods=['GET'])
api_bp.add_url_rule('/list-erds', 'list_erds', ERDController.list_erds, methods=['GET'])
api_bp.add_url_rule('/reload-system', 'reload_system', ERDController.reload_system, methods=['POST'])

# ERD generation and download routes
api_bp.add_url_rule('/generate-erd-image/<erd_name>', 'generate_erd_image', ERDController.generate_erd_image, methods=['GET'])
api_bp.add_url_rule('/download-erd/<filename>', 'download_erd', ERDController.download_erd, methods=['GET'])