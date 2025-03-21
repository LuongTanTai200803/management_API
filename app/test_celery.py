from app.celery_config import celery
from .routes.tasks import add_numbers  # Import trực tiếp task

result = add_numbers.apply(args=[1, 2, 3])

print("Task ID:", result.id)

