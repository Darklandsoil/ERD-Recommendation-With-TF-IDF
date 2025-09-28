import os

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
<<<<<<< HEAD
    UPLOAD_FOLDER = "static/image"
=======
    UPLOAD_FOLDER = "static"
>>>>>>> 76910b349d3d2a711428941bb7af86379989a9f2
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