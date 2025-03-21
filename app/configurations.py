from datetime import timedelta
import os

from flask import app

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("SECRET_KEY")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)  # Access Token hết hạn sau 15 phút
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # Refresh Token hết hạn sau 30 ngày
    JSONIFY_PRETTYPRINT_REGULAR = True  # Định dạng JSON đẹp
    app.json.ensure_ascii = False  # Tắt escape Unicode (quan trọng)
    # app.config['JSON_SORT_KEYS'] = False  # Tắt sắp xếp key trong JSON


    app.config['CELERY_CONFIG'] = {
    'task_serializer': 'json',
    'accept_content': ['json'],
    'result_serializer': 'json',
    'timezone': 'UTC',
    # 'broker_connection_retry_on_startup': True  # Thêm dòng này
    }

    # Cấu hình celery Beat
    from celery.schedules import crontab
    app.config['CELERY_BEAT_SCHEDULE'] = {
    'delete-overdue-tasks-every-hour': {
        'task': 'app.tasks.delete_overdue_tasks',
        'schedule': 30.0,  # Chạy mỗi giờ (3600 giây)
    },
    } 