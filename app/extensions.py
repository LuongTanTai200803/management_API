from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Khởi tạo db
db = SQLAlchemy()
# Khởi tạo đối tượng để quản lý JWT
jwt = JWTManager()