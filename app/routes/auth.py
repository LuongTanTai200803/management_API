from flask import Blueprint, request, jsonify
from app.models.models import User
from app.extensions import db
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    get_jwt, jwt_required, 
    get_jwt_identity
    )

from app.routes.admin import user
auth_bp = Blueprint("auth", __name__)

# from flask_jwt_extended import decode_token
# from datetime import datetime, timezone

# token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1..."  # Access token cần kiểm tra
# decoded_token = decode_token(token)

# exp_timestamp = decoded_token["exp"]  # Lấy thời gian hết hạn của token
# exp_datetime = datetime.fromtimestamp(exp_timestamp, timezone.utc)

# print(f"Token hết hạn lúc: {exp_datetime}")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"message": "User already exists"}), 400
    
    user = User(username=data["username"], role="admin")
    # Password hash rồi lưu vào db
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401
    print(f"user.: {user.id}, type: {type(user.id)}")
    print(f"user.username: {user.username}, type: {type(user.username)}")

    access_token = create_access_token(
        identity= user.username, 
        additional_claims = {"role": user.role}
    )
    refresh_token = create_refresh_token(identity= user.username,)

    user.access_token = access_token
    user.refresh_token = refresh_token
    # print(f"Updating user: {user.username}, access_token: {access_token}")
    db.session.commit()
    print(f"Received Token: {user.access_token}")  # 🔍 Debug xem Flask có nhận token không
    print(f"User role: {user.role}")
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        username = get_jwt_identity()  # Lấy usernametừ refresh_token

        user = User.query.filter_by(username=username).first()  
        if not user:
            print("[ERROR] User not found in database!", flush=True)
            return jsonify({"message": "User not found"}), 404

        # claims = get_jwt() Trả về toàn bộ claims  bao gồm role

        new_access_token = create_access_token(
            identity= user.username ,  # Đảm bảo identity là string
            additional_claims={"role": user.role}
        )
        return jsonify(access_token=new_access_token), 200

    except Exception as e:
        print(f"[ERROR] Exception Occurred: {str(e)}", flush=True)
        return jsonify({"message": "Internal Server Error"}), 500

@auth_bp.route('/get-token', methods=['GET'])
@jwt_required()  # Bảo vệ endpoint, chỉ user đã đăng nhập mới lấy được token
def get_token():
    username = get_jwt_identity()  # Lấy username từ token hiện tại
    user = User.query.filter_by(username=username).first()
    if not user or not user.access_token:
        return jsonify({"msg": "Token not found"}), 404
    return jsonify({"accessToken": user.access_token}), 200
