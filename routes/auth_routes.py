from flask import Blueprint
from controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Authentication routes
auth_bp.add_url_rule('/register', 'register', AuthController.register, methods=['POST'])
auth_bp.add_url_rule('/login', 'login', AuthController.login, methods=['POST'])
auth_bp.add_url_rule('/logout', 'logout', AuthController.logout, methods=['POST'])
auth_bp.add_url_rule('/me', 'me', AuthController.get_current_user, methods=['GET'])