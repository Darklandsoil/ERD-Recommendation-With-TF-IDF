import os

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    UPLOAD_FOLDER = "static/image"
    MONGODB_URI = os.environ.get('MONGODB_URI') or "mongodb://localhost:27017/"
    DATABASE_NAME = "Rekom_ERD"
    COLLECTION_NAME = "erd"
    
    # TF-IDF Configuration
    TFIDF_MAX_FEATURES = 1000
    TFIDF_NGRAM_RANGE = (1, 2)
    
    # Recommendation System Configuration
    DEFAULT_TOP_K = 10
    DEFAULT_MIN_SIMILARITY = 0.05

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}