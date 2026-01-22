#!/bin/bash

set -e

# 创建日志目录
LOG_DIR="${PWD}/logs"
mkdir -p "$LOG_DIR"

# 设置 PYTHONPATH
export PYTHONPATH=${PWD}:$PYTHONPATH

echo "启动 Celery worker..."
uv run celery -A app.tasks.celery_app.celery_app worker --loglevel=info > "$LOG_DIR/celery.log" 2>&1 &
CELERY_PID=$!

echo "启动 FastAPI 服务..."
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1 > "$LOG_DIR/uvicorn.log" 2>&1 &
UVICORN_PID=$!

# 捕获退出信号，优雅关闭服务
trap "echo '正在关闭服务...'; kill $CELERY_PID $UVICORN_PID; exit" SIGINT SIGTERM

# 等待服务进程
wait $CELERY_PID
wait $UVICORN_PID