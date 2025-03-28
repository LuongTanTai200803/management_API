from flask import Blueprint, request, jsonify
from app.models.models import User
from app.extensions import db
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    get_jwt, jwt_required, 
    get_jwt_identity
    )
import logging

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
    try:
        data = request.get_json()
        if not data:    # check missing data
            logging.warning("Register attempt with missing JSON data")
            return jsonify({"message": "Missing JSON data"}), 400
        
        username = data.get("username")
        password = data.get("password")
        logging.debug(f"Registration information: {username} & {password}")
        if not username or not password:   # Yếu cầu có 2 thông tin 
            logging.error(f"Register failed: missing username or password")
            return jsonify({"message": "Username and password required"}), 400
        
        if User.query.filter_by(username=data["username"]).first():
            logging.warning("User already exists")
            return jsonify({"message": "User already exists"}), 400
        
        user = User(username=data["username"], role="admin")
        # Password hash rồi lưu vào db
        user.set_password(data["password"])

        db.session.add(user)
        db.session.commit()
        logging.info(f"User {username} Register in successfully")
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        logging.error(f"Unexpected error occurred during registration: {str(e)}", exc_info=True)
        raise e
    
@auth_bp.route("/login", methods=["POST"])
def login():
    try:    
        data = request.get_json()
        logging.info(f"Login request received: {data}")  # Log dữ liệu nhận được
        if not data:
            logging.warning("Login attempt with missing JSON data")
            return jsonify({"message": "Missing JSON data"}), 400
        
        username = data.get("username")
        password = data.get("password")
        logging.debug(f"msg: {username} & {password}")
        if not username or not password:   # Yếu cầu có 2 thông tin 
            logging.error(f"Login failed: missing username or password")
            return jsonify({"message": "Username and password required"}), 400
        
        user = User.query.filter_by(username=data["username"]).first()

        if not user or not user.check_password(data["password"]):
            if user:
                logging.warning(f"Login failed: password not correct")
            else:
                logging.warning(f"Login failed: username not correct")
            return jsonify({"message": "Invalid credentials"}), 401
        # Ghi log moi khi user login
        logging.info(f"User {username} logged in successfully")

        access_token = create_access_token(
            identity= user.username, 
            additional_claims = {"role": user.role}
        )
        refresh_token = create_refresh_token(identity= user.username,)

        user.access_token = access_token
        user.refresh_token = refresh_token
        db.session.commit()

        logging.info(f"Tokens generated for {username}: Access token - {access_token[:10]}...")
        
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    except Exception as e:
        logging.error(f"Unexpected error in /login: {str(e)}", exc_info=True)
        return e 
    
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

