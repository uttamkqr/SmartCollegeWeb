"""
Configuration settings for Smart College Dashboard
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration"""

    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1'

    # Application
    APP_NAME = 'Smart College Dashboard'
    APP_VERSION = '2.0.0'

    # Session
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

    # File Upload
    UPLOAD_FOLDER = 'student_images'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    # Database
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME', 'smart_attendance')
    DB_POOL_SIZE = 5

    # Email
    EMAIL_USER = os.environ.get('EMAIL_USER')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    # Face Recognition
    FACE_RECOGNITION_THRESHOLD = 70  # Confidence threshold (0-100)
    MIN_FACE_SIZE = (30, 30)
    FACE_DETECTION_SCALE_FACTOR = 1.1
    FACE_DETECTION_MIN_NEIGHBORS = 5
    TRAINING_IMAGES_PER_STUDENT = 30

    # Attendance
    CLASS_START_TIME = '09:00'
    LATE_THRESHOLD_MINUTES = 15  # Minutes after class start to mark as late

    # Folders
    RECOGNIZER_FOLDER = 'recognizer'
    REPORTS_FOLDER = 'attendance_reports'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'app.log'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DB_NAME = 'smart_attendance_test'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """Get configuration based on environment"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    return config.get(config_name, config['default'])
