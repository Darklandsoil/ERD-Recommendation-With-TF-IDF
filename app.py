import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from config import config
from routes.main_routes import main_bp
from routes.api_routes import api_bp
from routes.auth_routes import auth_bp
from routes.request_routes import request_bp
from routes.admin_routes import admin_bp

def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # JWT Error Handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "error": "Token telah kadaluarsa",
            "message": "Silakan login kembali"
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "error": "Token tidak valid",
            "message": "Silakan login kembali"
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            "error": "Token tidak ditemukan",
            "message": "Akses ditolak. Silakan login terlebih dahulu"
        }), 401
    
    # Global Error Handlers
    @app.errorhandler(400)
    def bad_request_error(error):
        """Handle Bad Request errors (including invalid JSON)"""
        return jsonify({
            "error": "Bad Request",
            "message": "Request tidak valid. Periksa format data yang dikirim."
        }), 400
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle Not Found errors"""
        return jsonify({
            "error": "Not Found",
            "message": "Resource yang diminta tidak ditemukan"
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed_error(error):
        """Handle Method Not Allowed errors"""
        return jsonify({
            "error": "Method Not Allowed",
            "message": "Method HTTP tidak diizinkan untuk endpoint ini"
        }), 405
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle Internal Server errors"""
        return jsonify({
            "error": "Internal Server Error",
            "message": "Terjadi kesalahan pada server. Silakan coba lagi nanti."
        }), 500
    
    @app.before_request
    def validate_json():
        """Validate JSON for POST/PUT requests"""
        from flask import request
        if request.method in ['POST', 'PUT'] and request.is_json:
            try:
                # Try to parse JSON, will raise BadRequest if invalid
                request.get_json(force=True)
            except Exception:
                return jsonify({
                    "error": "Invalid JSON",
                    "message": "Format JSON tidak valid"
                }), 400
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(request_bp)
    app.register_blueprint(admin_bp)
    
    # Ensure upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True)