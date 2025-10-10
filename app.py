import os
from flask import Flask
from flask_jwt_extended import JWTManager
from config import config
from routes.main_routes import main_bp
from routes.api_routes import api_bp
from routes.auth_routes import auth_bp
from routes.request_routes import request_bp

def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(request_bp)
    
    # Ensure upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True)