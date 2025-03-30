import cv2
import numpy as np
from PIL import Image
import io

def run(file_path):
    img = cv2.imread(file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if 10 < area < 200:
            cv2.drawContours(binary, [contour], -1, (0, 0, 0), thickness=cv2.FILLED)

    result = cv2.bitwise_not(binary)

    _, buffer = cv2.imencode('.jpg', result)
    img_bytes = io.BytesIO(buffer)

    pil_img_for_ocr = Image.open(img_bytes)

    return pil_img_for_ocr