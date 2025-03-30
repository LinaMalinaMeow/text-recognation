import cv2

def is_cell_empty(image_path, intensity_threshold=50, pixel_threshold=0.01):
    cell_image = cv2.imread(image_path)
    gray_cell = cv2.cvtColor(cell_image, cv2.COLOR_BGR2GRAY)
    _, binary_mask = cv2.threshold(gray_cell, intensity_threshold, 255, cv2.THRESH_BINARY_INV)
    non_empty_pixels = cv2.countNonZero(binary_mask)
    non_empty_ratio = non_empty_pixels / gray_cell.size
    return non_empty_ratio < pixel_threshold