import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from app.models.models import User
from app.extensions import db
from flask_jwt_extended import create_access_token


def test_register(client, reset_db):
    
    """Test API đăng ký"""
    
    data = {"username": "admin","password": "123456"}
    response = client.post("/api/auth/register", json=data)

    assert response.status_code == 201  # Kiểm tra response code
    assert response.json["message"] == "User created successfully"

    # Kiểm tra user có trong database
    # with client.application.app_context():
    #     db.session.add(user)
    #     db.session.commit()

    # user = User.query.filter_by(username="admin").first()
    # assert user is not None  # Kiểm tra user được tạo
    # assert user.check_password("123456")  # Kiểm tra mật khẩu

def test_login(client):
    """Test API đăng nhập"""
    data = {
        "username": "admin",
        "password": "123456"
    }
    response = client.post("/api/auth/login", json=data)
    assert response.status_code == 200  # Kiểm tra response code
    # assert response.response.json = "Invalid credentials"
    # assert "access_token" in response.json  # Kiểm tra access_token tồn tại
    # assert "refresh_token" in response.json  # Kiểm tra refresh_token tồn tại

# def test_get_users(client, setup_users):
#     """Test API GET /api/admin/get với database test"""
#     user1, user2 = setup_users

#     with client.application.app_context():
#         access_token_1 = create_access_token(identity=str(user1.id), additional_claims={"role": "admin"})
#         access_token_2 = create_access_token(identity=str(user2.id), additional_claims={"role": "user"})

#     headers_1 = {"Authorization": f"Bearer {access_token_1}"}
#     headers_2 = {"Authorization": f"Bearer {access_token_2}"}

#     # Admin gọi API (phải thành công)
#     response_1 = client.get("/api/admin/get", headers=headers_1)
#     assert response_1.status_code == 200

#     # User gọi API (phải bị chặn)
#     response_2 = client.get("/api/admin/get", headers=headers_2)
#     assert response_2.status_code == 403
