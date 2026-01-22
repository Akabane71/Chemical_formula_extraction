# 思路
使用 minerU 进行 pdf识别 / azure dockment

使用 yolo 的 UniParser/MolDet 来提取分子式

使用 llm 来对 minerU 提取的 markdown 文件 进行分析，提取结构化数据

## 各个服务

1. ocr 服务 (可选)
### minerU 服务
> 提取文字的服务可以使用minerU的服务来批量提取成 markdown 格式
```bash
mineru-api --host 127.0.0.1 --port 8886
```

### Azure Document Intelligence
> azure 的文档识别服务



2. 图片提取
###  YOLO 提取


# 学习笔记：

##  celery 
kill掉 celery 的服务
```bash
pkill -f 'celery'
```

##  测试阶段
uv run uvicorn app.main:app

uv run app/tests/tasks/tests_yolo_process_pdf.py

构建 docker-img
```bash
docker build -t chemical-formula-extraction:latest .
```

```bash
docker run -d --name chemical-formula-extraction -p 8000:8000 chemical-formula-extraction:latest
```

##  新知识点：

PYTHONPATH = .