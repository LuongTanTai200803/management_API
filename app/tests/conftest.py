import os
import sys
import pytest
from unittest.mock import patch
from flask_jwt_extended import decode_token
from app.configurations import TestingConfig
from app.create_app import create_app
from app.extensions import db

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

@pytest.fixture
def mock_jwt(mocker):
    mock_payload = {
        "sub": 1,  # Giả lập user ID
        "role": "admin",
        "exp": 9999999999  # Token không hết hạn
    }
    
    mocker.patch("flask_jwt_extended.decode_token", return_value=mock_payload)

@pytest.fixture
def app():
    app, _, _ = create_app()
    app.config.from_object(TestingConfig())

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()

# def client(app):
#     with app.test_client() as client:
#         yield client
@pytest.fixture                 
def client(app):
    return app.test_client()

@pytest.fixture
def reset_db(app):
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
        db.session.commit()
