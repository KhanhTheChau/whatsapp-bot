# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

# Không ghi file .pyc, log stdout không bị buffer (quan trọng để xem log qua docker logs)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # Gunicorn ghi control socket vào $HOME/.gunicorn; trỏ HOME sang /tmp (tmpfs)
    # để container chạy được với read_only filesystem.
    HOME=/tmp

WORKDIR /app

# Cài dependencies trước, tách khỏi source code để tận dụng layer cache:
# sửa code sẽ không phải cài lại thư viện.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir "gunicorn>=21.2.0"

# Copy source code
COPY . .

# Chạy bằng user thường thay vì root cho an toàn
RUN useradd --create-home --uid 1000 appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

# 1 worker + nhiều thread: GeminiService lưu lịch sử chat in-memory theo process,
# nhiều worker sẽ làm user bị mất context khi request rơi vào process khác.
# Timeout 120s vì mỗi request phải chờ Gemini trả lời rồi mới gọi WhatsApp API.
CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "1", \
     "--threads", "8", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "main:app"]
