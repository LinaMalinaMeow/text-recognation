from ultralytics import YOLO
import numpy as np

conf_threshold = 0.5

def run(path):
    model = YOLO('table_recognize/cell_detect.pt')

    results = model(path, iou=0.1)

    cells = []

    for result in results:
        boxes = result.boxes
        filtered_boxes = boxes[boxes.conf >= conf_threshold]
        for box in filtered_boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cells.append((x1, y1, x2, y2))

    cells = sorted(cells, key=lambda b: (b[1], b[0]))

    average_height = np.mean([y2 - y1 for _, y1, _, y2 in cells])
    row_threshold = max(10, average_height * 0.1)
    width_threshold = max(20, average_height * 0.2)

    rows = []
    current_row = []
    current_y = None

    for cell in cells:
        x1, y1, x2, y2 = cell
        if current_y is None or abs(y1 - current_y) < row_threshold:
            current_row.append(cell)
            current_y = y1
        else:
            current_row = sorted(current_row, key=lambda c: c[0])
            rows.append(current_row)
            current_row = [cell]
            current_y = y1

    if current_row:
        current_row = sorted(current_row, key=lambda c: c[0])
        rows.append(current_row)

    completed_rows = []
    for row in rows:
        completed_row = []
        for i in range(len(row) - 1):
            completed_row.append(row[i])
            _, _, x2_current, _ = row[i]
            x1_next, _, _, _ = row[i + 1]
            if (x1_next - x2_current) > width_threshold:
                completed_row.append((x2_current, row[i][1], x1_next, row[i][3]))
        completed_row.append(row[-1])
        completed_rows.append(completed_row)

    return completed_rows