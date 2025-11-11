from flask import Blueprint
from controllers.request_controller import RequestController

request_bp = Blueprint('request', __name__, url_prefix='/api/requests')

# Request management routes
request_bp.add_url_rule('/', 'create_request', RequestController.create_request, methods=['POST'])
request_bp.add_url_rule('/my-requests', 'get_user_requests', RequestController.get_user_requests, methods=['GET'])
request_bp.add_url_rule('/<request_id>/cancel', 'cancel_request', RequestController.cancel_request, methods=['DELETE'])

# Advisor routes
request_bp.add_url_rule('/pending', 'get_pending_requests', RequestController.get_pending_requests, methods=['GET'])
request_bp.add_url_rule('/<request_id>/assign', 'assign_request', RequestController.assign_request, methods=['PUT'])
request_bp.add_url_rule('/my-assigned', 'get_advisor_requests', RequestController.get_advisor_requests, methods=['GET'])
request_bp.add_url_rule('/<request_id>/complete', 'complete_request', RequestController.complete_request, methods=['PUT'])