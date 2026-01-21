from celery import Celery
from app.core.config import rabbit_mq_settings

celery_app = Celery(
    "process_pdf",
    broker=f"amqp://{rabbit_mq_settings.RABBITMQ_USER}:{rabbit_mq_settings.RABBITMQ_PASSWORD}@{rabbit_mq_settings.RABBITMQ_HOST}:{rabbit_mq_settings.RABBITMQ_PORT}{rabbit_mq_settings.RABBITMQ_VHOST}",   # RabbitMQ 作为消息中间件
    backend="rpc://"                                   # 推荐用 rpc 或数据库等作为结果后端
)

# 可选：自动发现 tasks
celery_app.autodiscover_tasks(['app.tasks.yolo_process_pdf'])