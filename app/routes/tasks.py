from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from app.models.models import Task, User
from app.extensions import db

task_bp = Blueprint("tasks", __name__)

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
        user_id= user.id
        )

    # Nếu có description thì thêm vào
    task.description = data.get("description", "No description")
    db.session.add(task)
    db.session.commit()

    return jsonify({"message": "Task created successfully", "task_id": task.id}), 201

@task_bp.route("/", methods=["GET"])
@jwt_required() # Buộc user phải có token hợp lệ
def gets_task():
    claims = get_jwt()  # Lấy toàn bộ claims trong token
    token = request.headers.get("Authorization")
    print(f"Received Token: {token}")  # 🔍 Debug xem Flask có nhận token không
    print(f"User role: {claims.get('role')}")

    current_user = get_jwt_identity() # Lấy identity là username

    # truy xuất user để dùng cho các bước tiếp theo
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404
 
    if claims.get("role") == "admin":
        tasks = Task.query.all() # Lấy tất cả tasks
    elif claims.get("role") == "user":
        tasks = Task.query.filter_by(user_id=user.id).all()  # Lấy tất cả task của user_id = 1
    else:
        return jsonify({"msg": "Unauthorized role"}), 403
    
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

    return jsonify({"tasks": tasks_data}), 200  # Trả về danh sách id dưới dạng JSON
