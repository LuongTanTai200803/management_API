# Sử dụng Python làm base image
FROM python:3.11

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép file requirements vào container
COPY requirements.txt .

# Cài đặt các dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Mở cổng 5000
EXPOSE 5000

# Chạy ứng dụng Flask
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1","--log-level", "debug", "--access-logfile", "-", "--error-logfile", "-", "--timeout", "60", "run:app"]
