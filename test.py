from ultralytics import YOLO

model = YOLO('preprocess_crop.pt')

results = model('image copy.png', iou=0.1)

for result in results:
    result.show()