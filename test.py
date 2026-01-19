from ultralytics import YOLO
from pathlib import Path


model = YOLO("backend/static/moldet_yolo11l_640_general.pt")
results =model.predict(f"{Path(__file__).parent/ 'backend' / 'muck' / 'imgs' / '1.png'}", save=False, imgsz=640, conf=0.5)

for result in results:
    print(result.boxes.xyxy)
    print(result.boxes.conf)
    print(result.boxes.cls)