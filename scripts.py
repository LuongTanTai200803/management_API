from datetime import datetime, timedelta, timezone
import json
import requests

BASE_URL = "http://127.0.0.1:5000/api"
REGISTER_URL = f"{BASE_URL}/auth/register"
LOGIN_URL = f"{BASE_URL}/auth/login"
TASK_URL = f"{BASE_URL}/tasks/"
TASK_URL_CREATE = f"{BASE_URL}/tasks/"
TASK_URL_UPDATE = f"{BASE_URL}/tasks/d00fa6d8-5a43-4fb1-bbcf-cbf13af1c292"
TASK_URL_DELETE = f"{BASE_URL}/tasks/d9b821d2-e02c-47be-90b3-547a4e57e6a6"
TASK_URL_DELETE_OVERDUE = f"{BASE_URL}/tasks/delete-overdue"
TASK_CACHE = f"{BASE_URL}/tasks/cache"

# register_payload = {"username": "Khải", "password": "123456"}
# try:
#     register_payload = requests.post(REGISTER_URL, json=register_payload)
#     # print(f"Login status: {register_payload.status_code}")  # Kiểm tra status
#     # print(f"Login response: {register_payload.text}")       # Kiểm tra nội dung
# except requests.exceptions.ConnectionError:
#     print(f"Cannot connect to {REGISTER_URL}. Is the server running?")
#     exit()

# if register_payload.status_code != 201:
#     print(f"Login failed: {register_payload.text}")
#     exit()

login_payload = {"username": "Khải", "password": "123456"}
# Gọi /auth/login


try:
    login_response = requests.post(LOGIN_URL, json=login_payload)
    # print(f"Login status: {login_response.status_code}")  # Kiểm tra status
    # print(f"Login response: {login_response.text}")       # Kiểm tra nội dung
except requests.exceptions.ConnectionError:
    print(f"Cannot connect to {LOGIN_URL}. Is the server running?")
    exit()

if login_response.status_code != 200:
    print(f"Login failed: {login_response.text}")
    exit()

access_token = login_response.json()['access_token']
headers = {"Authorization": f"Bearer {access_token}"}
due_date = (datetime.now(timezone.utc) + timedelta(hours=7) +timedelta(hours=8)).isoformat()

# Gọi API auto xóa task quá hạn
# try:
#     delete_overdue = requests.post(TASK_URL_DELETE_OVERDUE, headers=headers)

#     print(f"Tasks status: {delete_overdue .status_code}")    # Kiểm tra status
#     print(f"Tasks response:", delete_overdue .text)

#     if delete_overdue.status_code == 200:  # Dùng 201 cho GET
#         print("Result:", delete_overdue.json())
#     else:
#         print(f"Tasks failed: {delete_overdue.text}")
# except requests.exceptions.ConnectionError:
#     print(f"Cannot connect to {TASK_URL_DELETE_OVERDUE}")
#     exit()
try:
    # Chú ý 
    # ('search', default='', type=str)  # Tìm kiếm theo title
    # ('page', default=1, type=int)      # Trang hiện tại
    # ('per_page', default=10, type=int)  # Số task mỗi trang
   
    get_response = requests.get(TASK_URL, headers=headers)

    print(f" - Status: {get_response.status_code}")
    print(f" - Tasks count: {len(get_response.json()['tasks'])}")
    print("-" * 50)
    if get_response.status_code == 200:  # Dùng 200 cho GET
        print("Result:", get_response.json())
    else:
        print(f"Get tasks failed: {get_response.text}")
except requests.exceptions.ConnectionError:
    print(f"Cannot connect to {TASK_URL}")
    exit()


# Check API create_task   
create_task = {
    "title": "Cài đặt Flask-Caching", 
    "status": "Đang làm",
    "due_date": due_date
}
try:
    create_task = requests.post(TASK_URL_CREATE, headers=headers, json=create_task)

    print(f"Tasks status: {create_task .status_code}")    # Kiểm tra status
    print(f"Tasks response:", create_task .text)

    if create_task.status_code == 201:  # Dùng 201 cho GET
        print("Result:", create_task.json())
    else:
        print(f"Tasks failed: {create_task.text}")
except requests.exceptions.ConnectionError:
    print(f"Cannot connect to {TASK_URL_CREATE}")
    exit()

# Check API update_task   
# update_task = {
#     "status": "Done",
#     "title": "Lich lam viec 1"
# }                   
# try:
#     update_response = requests.put(TASK_URL_UPDATE, headers=headers, json=update_task)

#     print(f"Tasks status: {update_response .status_code}")    # Kiểm tra status
#     print(f"Tasks response:", update_response .text)

#     if update_response.status_code == 201:  # Dùng 201 cho GET
#         print("Result:", update_response.json())
#     else:
#         print(f"Tasks failed: {update_response.text}")
# except requests.exceptions.ConnectionError:
#     print(f"Cannot connect to {TASK_URL_UPDATE}")
#     exit()


# Xóa task
# try:
#     delete_response = requests.delete(TASK_URL_DELETE, headers=headers)
#     print(f"Tasks status: {delete_response .status_code}")    # Kiểm tra status
#     print(f"Tasks response:", delete_response .text)

# except requests.exceptions.ConnectionError:
#     print(f"Cannot connect to {TASK_URL_DELETE}")
#     exit()


# Lấy danh sách task
try:
    # Chú ý 
    # ('search', default='', type=str)  # Tìm kiếm theo title
    # ('page', default=1, type=int)      # Trang hiện tại
    # ('per_page', default=10, type=int)  # Số task mỗi trang
   
    get_response = requests.get(TASK_URL, headers=headers)

    print(f" - Status: {get_response.status_code}")
    print(f" - Tasks count: {len(get_response.json()['tasks'])}")
    print("-" * 50)
    if get_response.status_code == 200:  # Dùng 200 cho GET
        print("Result:", get_response.json())
    else:
        print(f"Get tasks failed: {get_response.text}")
except requests.exceptions.ConnectionError:
    print(f"Cannot connect to {TASK_URL}")
    exit()

#  if response.status_code == 200:
#         try:
#             data = response.json()  # Chỉ parse JSON nếu response hợp lệ
#             print("Dữ liệu JSON:", data)
#         except requests.exceptions.JSONDecodeError:
#             print("Lỗi: Response không phải JSON hợp lệ")
#             print("Nội dung thực tế:", response.text)
#     else:
#         print(f"Lỗi HTTP {response.status_code}: {response.text}")