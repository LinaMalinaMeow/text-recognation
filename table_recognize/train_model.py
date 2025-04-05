from ultralytics import YOLO

model = YOLO("yolo11x.pt")

model.train(data="my_custom_dataset.yaml", epochs=100, imgsz=640)