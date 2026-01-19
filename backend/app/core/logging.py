# app/core/logging.py
from __future__ import annotations

import logging
import os
import sys
from typing import Optional

from loguru import logger


class InterceptHandler(logging.Handler):
    """Redirect standard logging records to Loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except Exception:
            level = record.levelno

        # 找到真正调用日志的位置（跳过 logging 模块栈）
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(
            depth=depth,
            exception=record.exc_info,
            lazy=True,
        ).log(level, record.getMessage())


def setup_loguru(
    level: str = "INFO",
    *,
    json: bool = False,
    log_dir: Optional[str] = None,
    app_name: str = "app",
) -> None:
    """
    Initialize Loguru and intercept std logging + uvicorn logs.

    - level: DEBUG/INFO/WARNING/ERROR
    - json: output JSON logs (good for ELK/Loki)
    - log_dir: if provided, also write rotating file logs
    """
    level = (level or "INFO").upper()

    # 1) 移除 Loguru 默认 handler，重新配置
    logger.remove()

    # 2) 控制台输出（stdout）
    # 生产上跑在容器里通常就打 stdout 给采集器
    logger.add(
        sys.stdout,
        level=level,
        enqueue=True,        # 多线程/异步更稳
        backtrace=False,     # 想更详细可 True（会更慢更啰嗦）
        diagnose=False,      # 同上
        serialize=json,      # True -> JSON
    )

    # 3) 文件输出（可选）
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        logger.add(
            os.path.join(log_dir, f"{app_name}.log"),
            level=level,
            rotation="50 MB",
            retention="7 days",
            compression="zip",
            enqueue=True,
            serialize=json,
        )

    # 4) 接管标准 logging：root logger -> InterceptHandler
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(level)

    # 5) 把现有 logger（第三方/库）也统一改成 InterceptHandler
    #    避免某些库自己加 handler 导致重复输出
    for name in list(logging.root.manager.loggerDict.keys()):
        log = logging.getLogger(name)
        log.handlers = [InterceptHandler()]
        log.propagate = False

    # 6) 特别处理 uvicorn（最重要）
    # uvicorn.error / uvicorn.access 默认自己有 handler，不处理会出现“格式不统一/重复打印”
    for uvicorn_logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        uvicorn_logger = logging.getLogger(uvicorn_logger_name)
        uvicorn_logger.handlers = [InterceptHandler()]
        uvicorn_logger.propagate = False

    logger.bind(app=app_name).info("Loguru logging initialized | level={} | json={}", level, json)
