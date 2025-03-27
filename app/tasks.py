from celery import shared_task
from flask import current_app
from app.celery_config import make_celery

# Gửi mail thật
# @celery.task
# def send_task_creation_email(user_email, task_title):
#     from flask_mail import Message
#     with app.app_context():
#         msg = Message(
#             subject="New Task Created",
#             recipients=[user_email],
#             body=f"A new task '{task_title}' has been created."
#         )
#         mail.send(msg)
#         print(f"Sending email to {user_email} for task '{task_title}'")
#     return f"Email sent to {user_email}"

# Gửi mail ảo
@shared_task
def send_task_creation_email(user_email, task_title):
    from flask_mail import Message
    print(f"Sending email to {user_email} for task '{task_title}'")
    return f"Email sent to {user_email}"

@shared_task
def delete_overdue_tasks():
    from app.models.models import Task
    from app.extensions import db
    from datetime import datetime, timezone, timedelta
    # Lấy thời gian hiện tại ở UTC
    now_utc = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=7)))

    with current_app.app_context():
        overdue_tasks = Task.query.filter(Task.due_date < now_utc).all()
        for task in overdue_tasks:
            db.session.delete(task)
        db.session.commit()
        current_app.extensions['cache'].delete("all_tasks")
    return f"Deleted {len(overdue_tasks)} overdue tasks"

