from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_mail import Mail

# Khởi tạo db
db = SQLAlchemy()
# Khởi tạo đối tượng để quản lý JWT
jwt = JWTManager()
# Khởi tạo đối tượng mail
mail = Mail()
# Khởi tạo đối tượng cache
cache = Cache()