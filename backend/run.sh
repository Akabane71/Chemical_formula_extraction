#!/bin/bash

# 启动 Celery worker（后台运行，日志输出到 celery.log）
uv run celery -A app.tasks.celery_app.celery_app worker --loglevel=info > ${PWD}/logs/celery.log 2>&1 &

# 启动 FastAPI 服务
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1 > ${PWD}/logs/uvicorn.log 2>&1