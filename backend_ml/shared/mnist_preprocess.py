import cv2
import numpy as np
import os

def rec_digit(pil_image, show_image=False):
    os.makedirs('images_for_ds', exist_ok=True)
    image = np.array(pil_image.convert('L'))
    
    _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    min_contour_area = 5
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

    if filtered_contours:
        largest_contour = max(filtered_contours, key=cv2.contourArea)
        
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        margin = 4
        x, y = max(x - margin, 0), max(y - margin, 0)
        w, h = min(w + 2 * margin, image.shape[1] - x), min(h + 2 * margin, image.shape[0] - y)
        
        roi = image[y:y+h, x:x+w]

        mnist_image = np.zeros((28, 28), dtype=np.uint8)
        
        scale = 20.0 / max(roi.shape)
        new_w, new_h = int(roi.shape[1] * scale), int(roi.shape[0] * scale)
        resized_roi = cv2.resize(roi, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
        
        x_offset = (28 - new_w) // 2
        y_offset = (28 - new_h) // 2
        mnist_image[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized_roi

        mnist_image = mnist_image.astype('float32') / 255.0

        mnist_image[mnist_image > 0] = 1.0

        mnist_image = np.expand_dims(mnist_image, axis=0)

        mnist_image = mnist_image.astype('float32')

        return mnist_image

    else:
        raise ValueError("Нет подходящих контуров на изображении")