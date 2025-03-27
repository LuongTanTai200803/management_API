import os
import sys

from flask_jwt_extended import create_access_token
from app.models.models import User

import logging
from app.utils.decorators import *
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '...','...')))

# def test_get_user_success(mocker):
#     # Mock SQLAlchemy query
#     mock_query = mocker.patch('app.models.User.query')
#     mock_user = mocker.Mock()
#     mock_user.id = 1
#     mock_user.username = "john_doe"
#     mock_query.get.return_value = mock_user
    
#     # Tạo ứng dụng
#     app = create_app()
#     client = app.test_client()
    
#     # Gửi request
#     response = client.get('/api/user/1')
    
#     # Kiểm tra kết quả
#     assert response.status_code == 200
#     assert response.json == {"id": 1, "username": "john_doe"}
#     mock_query.get.assert_called_once_with(1)

# def test_get_user_not_found(mocker):
#     # Mock SQLAlchemy query
#     mock_query = mocker.patch('app.models.User.query')
#     mock_query.get.return_value = None
    
#     # Tạo ứng dụng
#     app = create_app()
#     client = app.test_client()
    
#     # Gửi request
#     response = client.get('/api/tasks/999')
    
#     # Kiểm tra kết quả
#     assert response.status_code == 404
#     assert response.json == {"error": "User not found"}
#     mock_query.get.assert_called_once_with(999)

def test_get_users(mocker, client):
    mock_query = mocker.patch('app.models.models.User.query')
    mock_user = [
        mocker.Mock(id=1 , username="admin"),
        mocker.Mock(id=2 , username="user" )
    ]
    mock_query.all.return_value = mock_user
      # Tạo token test
      
    with client.application.app_context():
        access_token_1 = create_access_token(
            identity=str(mock_user[0].id),
            additional_claims={"role": "admin"}
            )
        access_token_2 = create_access_token(
            identity=str(mock_user[1].id),
            additional_claims={"role": "user"}
            )
    headers_1 = {"Authorization": f"Bearer {access_token_1}"}
    headers_2 = {"Authorization": f"Bearer {access_token_2}"}
    with client:
        response_1 = client.get("/api/admin/get", headers=headers_1)
        response_2 = client.get("/api/admin/get", headers=headers_2)

    logging.debug(f"Response: {response_1}")
    assert response_1.status_code == 200, response_1.get_json()
    assert response_2.status_code == 403

    data_1 = response_1.get_json()
    data_2 = response_2.get_json()
    assert len(data_1) == 2
    # assert "role" in data_1, f"Unexpected response: {data_1}"

    # assert data_1["username"] == "admin"