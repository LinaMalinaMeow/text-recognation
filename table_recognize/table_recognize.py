from ultralytics import YOLO

# Функция которая возвращается массив координат каждой строки
def run(path):
    model = YOLO('table_recognize/cell_detect.pt')

    results = model(path, iou=0.1)

    cells = []

    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cells.append((x1, y1, x2, y2))

    cells = sorted(cells, key=lambda b: (b[1], b[0]))

    rows = []
    current_row = []
    current_y = None
    row_threshold = 10

    for cell in cells:
        x1, y1, x2, y2 = cell
        if current_y is None or abs(y1 - current_y) < row_threshold:
            current_row.append(cell)
            current_y = y1
        else:
            current_row = sorted(current_row, key=lambda b: b[0])
            rows.append(current_row)
            current_row = [cell]
            current_y = y1

    if current_row:
        current_row = sorted(current_row, key=lambda b: b[0])
        rows.append(current_row)
    
    return rows