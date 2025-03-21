from datetime import timedelta
from app import celery, mail, app
from flask_mail import Message  # Thêm Flask-Mail

# Gửi mail thật
# @celery.task
# def send_task_creation_email(user_email, task_title):
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
@celery.task
def send_task_creation_email(user_email, task_title):
    print(f"Sending email to {user_email} for task '{task_title}'")
    return f"Email sent to {user_email}"

@celery.task
def delete_overdue_tasks():
    from app.models.models import Task
    from app.extensions import db
    from datetime import datetime, timezone, timedelta
    # Lấy thời gian hiện tại ở UTC
    now_utc = datetime.now(timezone.utc)

    with app.app_context():
        overdue_tasks = Task.query.filter(Task.due_date < now_utc.astimezone(timezone(timedelta(hours=7)))).all()
        for task in overdue_tasks:
            db.session.delete(task)
        db.session.commit()
    return f"Deleted {len(overdue_tasks)} overdue tasks"