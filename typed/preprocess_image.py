import cv2
import numpy as np
from PIL import Image
import io
import matplotlib.pyplot as plt

def run(file_path):
    inBlack = np.array([170, 170, 170], dtype=np.float32)
    inWhite = np.array([255, 255, 255], dtype=np.float32)
    inGamma = np.array([1.0, 1.0, 1.0], dtype=np.float32)
    outBlack = np.array([0, 0, 0], dtype=np.float32)
    outWhite = np.array([255, 255, 255], dtype=np.float32)

    img = cv2.imread(file_path)
    int8 = cv2.convertScaleAbs(img)

    color_level = np.clip((int8 - inBlack) / (inWhite - inBlack), 0, 255)
    color_level = (color_level ** (1 / inGamma)) * (outWhite - outBlack) + outBlack
    color_level = np.clip(color_level, 0, 255).astype(np.uint8)

    gray_image = cv2.cvtColor(color_level, cv2.COLOR_BGR2GRAY)

    _, threshold = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    inverted = cv2.bitwise_not(threshold)

    _, buffer = cv2.imencode('.jpg', inverted)
    img_bytes = io.BytesIO(buffer)

    pil_img_for_ocr = Image.open(img_bytes)

    return pil_img_for_ocr