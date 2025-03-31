# Sử dụng Python làm base image
FROM python:3.11

# Đặt thư mục làm việc trong container
WORKDIR /app

# Cài thêm công cụ kiểm tra mạng
RUN apt update && apt install -y net-tools iproute2

# Sao chép file requirements vào container
COPY requirements.txt .

# Cài đặt các dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Gunicorn chạy trên cổng 8000
EXPOSE 8000     

# Chạy ứng dụng Flask (4w, 2thread )
CMD ["gunicorn", "--workers", "4", "--threads", "2", "--bind", "0.0.0.0:8000", "--log-level", "info", "--access-logfile", "-", "--error-logfile", "-", "--timeout", "60", "run:app"]