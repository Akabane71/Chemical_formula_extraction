from celery import Celery
from app.core.config import rabbit_mq_settings,mongodb_settings

celery_app = Celery(
    "process_pdf",
    # RabbitMQ 作为消息中间件
    broker=f"amqp://{rabbit_mq_settings.RABBITMQ_USER}:{rabbit_mq_settings.RABBITMQ_PASSWORD}@{rabbit_mq_settings.RABBITMQ_HOST}:{rabbit_mq_settings.RABBITMQ_PORT}{rabbit_mq_settings.RABBITMQ_VHOST}",   
    # MongoDB 作为结果后端
    backend=f"mongodb://{mongodb_settings.MONGODB_USER}:{mongodb_settings.MONGODB_PASSWORD}@{mongodb_settings.MONGODB_HOST}:{mongodb_settings.MONGODB_PORT}"                                   
)

# 自动发现 tasks
celery_app.autodiscover_tasks(['app.tasks.yolo_process_pdf', 'app.tasks.ocr_process_pdf'])


async def get_task_result_action(task_id: str):
    """
    获取 Celery 任务结果
    """
    from app.tasks.yolo_process_pdf import celery_app
    result = celery_app.AsyncResult(task_id)
    if result.ready():
        res = result.result
        # 如果是异常对象，返回字符串
        if isinstance(res, Exception):
            return {"error": str(res)}
        return res
    else:
        return None