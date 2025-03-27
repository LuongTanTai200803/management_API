from app.create_app import create_app


# Tạo ứng dụng và các thành phần liên quan
app, celery, migrate = create_app()