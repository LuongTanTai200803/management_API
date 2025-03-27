from flask import Blueprint

# Blueprint tổng của API
api_bp = Blueprint("api", __name__)

# Import từng module route
from .admin import admin_bp
from .auth import auth_bp
from .tasks import task_bp


# Đăng ký vào Blueprint tổng
api_bp.register_blueprint(admin_bp, url_prefix="/admin")
api_bp.register_blueprint(auth_bp, url_prefix="/auth")
api_bp.register_blueprint(task_bp, url_prefix="/tasks")

def register_routes(app):
    app.register_blueprint(api_bp, url_prefix="/api")