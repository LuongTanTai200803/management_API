from functools import wraps
import json
import traceback
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask import Response, current_app, jsonify, request
import logging

# Cấu hình logging
if not logging.getLogger().hasHandlers():
    logging.basicConfig(
        filename='api_log.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def role_required(required_role):
    """
    Decorator kiểm tra vai trò của user dựa trên JWT claims.
    :param required_role: Vai trò cần thiết để truy cập (e.g., 'admin', 'user')
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()     # Lấy thông tin từ JWT token
            # Kiểm tra vai trò
            if claims.get("role") != required_role:
                logging.error(f"Access denied - Role mismatch. User role: {claims.get("role")}, Required role: {required_role}")
                return jsonify({"message": "Access forbidden",
                                "current role": claims.get("role"),
                                "current role required": required_role
                                }), 403
            
            # Nếu đúng role, tiếp tục thực thi hàm
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def api_handler(func):
    """
    Decorator xử lý logging và error handling cho API endpoints.
    """
   
    @wraps(func)
    def wrapper(*args, **kwargs):
        endpoint = request.path
        method = request.method
        user_id = get_jwt_identity()  # Lấy ID user từ token
        result = None
        try:
            # Ghi log request
            logging.info(f"Request - Endpoint: {endpoint} | Method: {method} | User: {user_id}")
            # Thực thi hàm API
            result = func(*args, **kwargs)

            # Kiểm tra nếu result là một tuple chứa (response, status_code)
            if isinstance(result, tuple) and len(result) == 2:
                response, status_code = result
                # Kiểm tra nếu response là một dict hay list
                if isinstance(response, (dict, list)): 
                    response = jsonify(response)
                # Ghi log thành công
                logging.info(f"Success - Endpoint: {endpoint} | Method: {method} | Response: {response.get_data(as_text=True)}")
                return response, status_code
            
            if isinstance(result, list):
                logging.info(f"Success - Endpoint: {endpoint} | Method: {method} | Response: {result}")
                return jsonify(result)  # Trả về JSON list

            # Ghi log thành công
            logging.info(f"Success - Endpoint: {endpoint} | Method: {method} | Response: {result}")
            
            return result
        except ValueError as val_err:
            # Xử lý lỗi validation
            logging.error(f"Validation Error - Endpoint: {endpoint} | Detail: {str(val_err)}")
            return jsonify({"error": str(val_err)}), 400
        
        except Exception as e:
            # Xử lý lỗi không mong muốn
            # error_message = f"Unexpected Error - Endpoint: {endpoint} | Detail: {str(e)}"
            # if result:
            #     error_message += f" | Response: {result}"
            # logging.error(error_message)
            logging.error(f"Unexpected Error - Endpoint: {endpoint} | Detail: {str(e)} | Response: {result}")
            print(f"Error: {str(e)}")  # Debug lỗi
            print(f"Error: {str(e)} - Traceback: {traceback.format_exc()}")
            # response = Response(
            #     json.dumps(({"error": "Lỗi server"}), ensure_ascii=False),
            #     mimetype='application/json'
            # )
            # return response
            return jsonify({"error": "Lỗi server"}), 500
    return wrapper
