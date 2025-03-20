from datetime import timedelta
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "occorps")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "mysql+pymysql://root:3366@localhost/my_project_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("SECRET_KEY", "occorps")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)  # Access Token hết hạn sau 15 phút
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # Refresh Token hết hạn sau 30 ngày