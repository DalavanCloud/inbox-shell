import os

FRONTDESK_HOST = os.environ.get('FRONTDESK_HOST', '127.0.0.1:80')
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'guest@127.0.0.1:5672')
MONITORING_FOLDER = os.environ.get('MONITORING_FOLDER', '/home/ftpuser')
SAFE_MODE = os.environ.get('SAFE_MODE', False)
LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'DEBUG')
