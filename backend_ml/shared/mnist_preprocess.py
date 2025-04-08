import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def rec_digit(pil_image, show_image=False):
    image = np.array(pil_image.convert('L'))

    _, image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        
        x, y, w, h = cv2.boundingRect(largest_contour)
        roi = image[y:y+h, x:x+w]

        mnist_image = np.zeros((28, 28), dtype=np.uint8)
        
        scale = 20.0 / max(w, h)
        new_w, new_h = int(w * scale), int(h * scale)
        resized_roi = cv2.resize(roi, (new_w, new_h), interpolation=cv2.INTER_AREA)
        
        x_offset = (28 - new_w) // 2
        y_offset = (28 - new_h) // 2
        mnist_image[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized_roi

        mnist_image = mnist_image.astype('float32') / 255.0

        mnist_image = np.expand_dims(mnist_image, axis=-1)
        
        mnist_image = np.expand_dims(mnist_image, axis=0)

        if show_image:
            plt.imshow(mnist_image.squeeze(), cmap='gray')
            plt.title('MNIST Format Image')
            plt.axis('off')
            plt.show()

        return mnist_image
    
    else:
        raise ValueError("No contours found in the image")