SQLALCHEMY_DATABASE_URI = "sqlite:///ticketShow.db"
SECRET_KEY = "LEarNIg"
SECURITY_PASSWORD_SALT = "salt"
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED =False
SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'

CELERY_BROKER_URL = "redis://localhost:6379/1"
CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
CELERY_TIMEZONE = "Asia/Kolkata"
REDIS_URL = "redis://localhost:6379/0"
