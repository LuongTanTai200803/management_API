from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
# from app.error_handlers import register_error_handlers
from app.models.models import User
from app.utils.decorators import api_handler, role_required
from app.extensions import db
from app.exceptions import BadRequestException, NotFoundException

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@role_required("admin")  # Chỉ admin mới truy cập được
def admin_dashboard():
    return jsonify({"message": "Welcome, Admin!"})

@admin_bp.route("/user", methods=["GET"])
@jwt_required()
@role_required("User")
def user():
    return jsonify({"message": "Welcome, User!"})

# admin set role
@admin_bp.route("/setrole", methods=["PUT"])
@jwt_required()
@role_required("user")  # Chỉ admin mới truy cập được
@api_handler
def admin_set_role():
    current_user = get_jwt_identity() # Lấy username từ token
    data = request.get_json()
    # Chắc chắn có 2 trường dữ liệu username và role
    if not data or "role" not in data:
        raise BadRequestException("Invalid request data")
    
    user = User.query.filter_by(username=current_user).first()

    if not user:
        raise NotFoundException("User not found")
    
    user.role = data.get("role")
    db.session.commit()
    return jsonify({"message": "Role updated"}), 201

@admin_bp.route("/get", methods=["GET"])
@jwt_required()
@role_required("admin")  # Chỉ admin mới truy cập được
@api_handler
def admin_get_users():
    current_user = get_jwt_identity() # Lấy username từ token

    user = User.query.filter_by(username=current_user).first()
    if not user:
        raise NotFoundException("User not found")
    
    users = User.query.all()
    response = [{
        "id": u.id,
        "username": u.username
    } for u in users]

    print(f"Header: {request.headers}")
    return jsonify(response), 200
