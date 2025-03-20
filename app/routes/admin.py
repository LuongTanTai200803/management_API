from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
import app
from app.models.models import User
from app.utils.decorators import role_required
from app.extensions import db

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
@role_required("admin")  # Chỉ admin mới truy cập được
def admin_set_role():
    data = request.get_json()
    # Chắc chắn có 2 trường dữ liệu username và role
    if not data or "username" not in data or "role" not in data:
        return jsonify({"message": "Invalid requets data"}), 400
    
    user = User.query.filter_by(username=data["username"]).first()

    if not user:
        return jsonify({"message": "User not found"}), 404
    
    VALID_ROLE = ["admin", "user", "guest"]
    if data["role"] not in VALID_ROLE:
        return jsonify({"message": "Invalid role"}), 400
    user.role = data.get("role")
    db.session.commit()
    return jsonify({"message": "Role updated"}), 201

