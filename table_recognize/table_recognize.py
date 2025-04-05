from ultralytics import YOLO
import numpy as np

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

    row_threshold = 10
    isolation_threshold = 80
    width_threshold = 20

    filtered_cells = []
    for i, cell in enumerate(cells):
        x1, y1, x2, y2 = cell
        neighboring_cells = [
            1 for cx1, cy1, _, _ in cells
            if np.sqrt((x1 - cx1) ** 2 + (y1 - cy1) ** 2) < isolation_threshold and (cx1, cy1) != (x1, y1)
        ]
        if len(neighboring_cells) >= 1:
            filtered_cells.append(cell)

    rows = []
    current_row = []
    current_y = None

    for cell in filtered_cells:
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