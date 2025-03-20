from functools import wraps
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask import jsonify

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt() 
            if claims.get("role") == "admin":
                return jsonify({"message": "Access forbidden"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

