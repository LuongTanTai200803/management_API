import jwt
import base64
import json
from datetime import datetime

# Token JWT
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjQ2NzczMSwianRpIjoiNjMyOGU5OTAtODUxYy00M2EzLTllMmItNzcxYmM2ZTY1ZWUwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IlRcdTAwZTBpIiwibmJmIjoxNzQyNDY3NzMxLCJjc3JmIjoiYWI2MjA2MTEtMzQxYi00MmJjLWI0OTAtNTFiMjI2MjYxNTMyIiwiZXhwIjoxNzQyNDY4NjMxLCJyb2xlIjoidXNlciJ9.dRcejLSUEQA3hyO2Ir0qswaqg-74q7FFpvgcCHHRNK"

# Khóa bí mật (thay bằng khóa thực tế nếu bạn có)
secret_key = "occorps"  # Ví dụ, thay bằng khóa thực tế của bạn

# Giải mã token không kiểm tra chữ ký (chỉ để xem payload)
def decode_jwt_payload(token):
    # Tách phần payload (phần thứ 2)
    payload_encoded = token.split('.')[1]
    # Thêm padding nếu cần (JWT base64 cần padding bằng '=')
    payload_encoded += '=' * (-len(payload_encoded) % 4)
    # Giải mã base64
    payload_decoded = base64.urlsafe_b64decode(payload_encoded).decode('utf-8')
    return json.loads(payload_decoded)

# Giải mã và kiểm tra chữ ký (nếu có khóa đúng)
def decode_jwt_with_signature(token, secret_key):
    try:
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
        return decoded
    except jwt.InvalidSignatureError:
        return "Chữ ký không hợp lệ. Kiểm tra lại khóa bí mật."
    except jwt.ExpiredSignatureError:
        return "Token đã hết hạn."
    except Exception as e:
        return f"Lỗi: {str(e)}"

# In thông tin payload mà không cần khóa
print("Payload (không kiểm tra chữ ký):")
payload = decode_jwt_payload(token)
print(json.dumps(payload, indent=4))

# Chuyển timestamp thành ngày giờ
iat = datetime.utcfromtimestamp(payload['iat']).strftime('%Y-%m-%d %H:%M:%S UTC')
exp = datetime.utcfromtimestamp(payload['exp']).strftime('%Y-%m-%d %H:%M:%S UTC')
print(f"Thời gian phát hành (iat): {iat}")
print(f"Thời gian hết hạn (exp): {exp}")
print(f"Vai trò (role): {payload['role']}")

# Kiểm tra chữ ký (nếu bạn có khóa đúng)
print("\nKiểm tra với khóa bí mật:")
result = decode_jwt_with_signature(token, secret_key)
print(result)