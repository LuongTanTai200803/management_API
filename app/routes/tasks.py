from collections import OrderedDict
from flask import Blueprint , jsonify, request, Response, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from app.models.models import Task, User
from app.extensions import db, cache
from app.tasks import delete_overdue_tasks, send_task_creation_email
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

task_bp = Blueprint("tasks", __name__)

@task_bp.route('/test',methods=["GET"])
def test():
    return{"msg": "OK"}

@task_bp.route("/", methods=["POST"])
@jwt_required() # Buộc user phải có token hợp lệ
def create_task():
    # token = request.headers.get("Authorization")
    # print(f"Received Token: {token}")  # 🔍 Debug xem Flask có nhận token không

    current_user = get_jwt_identity() # Lấy username từ token

    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({"msg": "User not found"}), 400
    data = request.get_json()

    task = Task(
        title=data["title"], 
        status=data["status"],
        due_date=data["due_date"],  
        user_id= user.id
        )

    # Nếu có description thì thêm vào
    task.description = data.get("description", "No description")
    db.session.add(task)
    db.session.commit()
    cache.delete(f"tasks_{user.id}")
    
    # Gọi Celery task
    send_task_creation_email.delay("example@gmail.com", task.title)

    return jsonify({"message": "Task created successfully", "task_id": task.id}), 201

@task_bp.route("/", methods=["GET"])
@jwt_required() # Buộc user phải có token hợp lệ
def gets_task():
    claims = get_jwt()  # Lấy toàn bộ claims trong token
    # token = request.headers.get("Authorization")
    # print(f"Received Token: {token}")  # 🔍 Debug xem Flask có nhận token không
    # print(f"User role: {claims.get('role')}")

    current_user = get_jwt_identity() # Lấy identity là username

    # truy xuất user để dùng cho các bước tiếp theo
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    # Lấy query parameters
    search = request.args.get('search', default='', type=str)  # Tìm kiếm theo title
    page = request.args.get('page', default=1, type=int)      # Trang hiện tại
    per_page = request.args.get('per_page', default=10, type=int)  # Số task mỗi trang
   
    # Xây dựng query cơ bản
    if claims.get("role") == "admin":
        query = Task.query # Lấy tất cả tasks
    elif claims.get("role") == "user":
        query = Task.query.filter_by(user_id=user.id)  # Lấy tất cả task của user_id = 1
    else:
        return jsonify({"msg": "Unauthorized role"}), 403
    
    # Thêm điều kiện search
    if search:
        query = query.filter(Task.title.ilike(f'%{search}%'))  # Tìm kiếm không phân biệt hoa thường
    
    query = query.order_by(Task.id.asc())  # Sắp xếp theo ID tăng dần
    # Thêm phân trang
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    tasks = pagination.items  # Danh sách task trong trang hiện tại

    # Chuyển đổi dữ liệu task
    tasks_data = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "users_id": task.user_id,
            "username": user.username
        }
        for task in tasks
    ]

   # Trả về kết quả với thông tin phân trang
    response =  OrderedDict ([
        ("tasks", tasks_data),              # Tổng số task
        ("total", pagination.total),        # Tổng số trang
        ("pages", pagination.pages),        # Trang hiện tại
        ("current_page", pagination.page) 
    ])
    # json_response = json.dumps( response, ensure_ascii=False)
    return jsonify(response), 200


@task_bp.route("/<task_id>", methods=["PUT"])
@jwt_required() # Buộc user phải có token hợp lệ
def update_task(task_id):
    current_user = get_jwt_identity() # Lấy username từ token
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({"msg": "User not found"}), 400
    # Kiểm tra có task hay không
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"msg": "Task not found"}), 404
    # Kiểm tra đúng user không
    if task.user_id != user.id:
        return jsonify({"msg": "Bạn không có quyền truy cập task này",
                        "Đây là task của user": task.user_id,
                        "user đang login là:": user.id
                        }), 403
    
    data = request.get_json()

    task.title = data.get("title", task.title)
    task.status = data.get("status", task.status)
    task.description = data.get("description", task.description)
    cache.delete(f"tasks_{user.id}")
    db.session.commit()

    return jsonify({
        "message": "Task update successfully",
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "user_id": task.user_id,
        }
    }), 201

@task_bp.route("/<task_id>", methods=["DELETE"])
@jwt_required() # Buộc user phải có token hợp lệ
def delete_task(task_id):
    current_user = get_jwt_identity() # Lấy username từ token
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({"msg": "User not found"}), 400
    # Kiểm tra có task hay không
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"msg": "Task not found"}), 404
    # Kiểm tra đúng user không
    if task.user_id != user.id:
        return jsonify({"msg": "Bạn không có quyền truy cập task này",
                        "Đây là task của user": task.user_id,
                        "user đang login là:": user.id
                        }), 403
    
    db.session.delete(task)
    db.session.commit()
    cache.delete(f"tasks_{user.id}")
    return jsonify({"message": "Task delete successfully"}), 201

@task_bp.route("/delete-overdue", methods=["POST"])
@jwt_required() # Buộc user phải có token hợp lệ
def delete_overdue():
    current_user = get_jwt_identity() # Lấy username từ token
    user = User.query.filter_by(username=current_user).first()
    task_result = delete_overdue_tasks.delay()  # Gửi task đến Celery
    send_task_creation_email.delay("example@gmail.com", task_result.id)
    cache.delete(f"tasks_{user.id}")
    return jsonify({"message": "Task is being processed", "task_id": task_result.id}), 200

@task_bp.route('/cache', methods=['GET'])
@cache.cached(timeout=10, key_prefix="tasks_cache")
def get_tasks():
    logger.info("Fetching tasks from database")  # Chỉ chạy khi không dùng cache
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks]), 200

# @task_bp.route('/cache', methods=['GET'])
# @cache.cached(timeout=16, key_prefix="tasks_cache")
# def get_tasks():
#     from datetime import datetime
#     return jsonify({"time": datetime.now().isoformat()})


