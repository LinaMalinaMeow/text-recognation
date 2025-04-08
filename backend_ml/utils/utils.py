from PIL import Image
import cv2
import numpy as np

def is_cell_empty(pil_image, intensity_threshold=140, pixel_threshold=0.01, central_fraction=0.9):
    cell_image = np.array(pil_image)

    if cell_image.ndim == 3 and cell_image.shape[2] == 3:
        cell_image = cv2.cvtColor(cell_image, cv2.COLOR_RGB2BGR)

    gray_cell = cv2.cvtColor(cell_image, cv2.COLOR_BGR2GRAY)

    height, width = gray_cell.shape

    h_start = int(height * (1 - central_fraction) / 2)
    h_end = int(height * (1 + central_fraction) / 2)
    w_start = int(width * (1 - central_fraction) / 2)
    w_end = int(width * (1 + central_fraction) / 2)

    central_region = gray_cell[h_start:h_end, w_start:w_end]

    _, binary_mask = cv2.threshold(central_region, intensity_threshold, 255, cv2.THRESH_BINARY_INV)

    non_empty_pixels = cv2.countNonZero(binary_mask)
    non_empty_ratio = non_empty_pixels / central_region.size

    return non_empty_ratio < pixel_threshold