from keras import models
import numpy as np
import sys
import os
from PIL import Image  # Для работы с изображениями
import random
import time  # Для генерации уникальных имен файлов
# todo: сделать нормально
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared import mnist_preprocess

# Вычислено эмпирическим путем
MAX_RECOGNATION_PERCENT = 0.8

def run(pil_image):
    prepared_image = mnist_preprocess.rec_digit(pil_image)

    model = models.load_model('mnist/best_model_test1.h5')

    prediction = model.predict(prepared_image)

    max_predict = np.amax((prediction[0]))

    predicted_class = np.argmax(prediction, axis=1)

    print(max_predict, predicted_class)

    if max_predict < MAX_RECOGNATION_PERCENT:
        low_predictions_dir = os.path.join(os.path.dirname(__file__), 'low_predictions')
        os.makedirs(low_predictions_dir, exist_ok=True)

        timestamp = int(time.time() * 1000)
        image_path = os.path.join(low_predictions_dir, f'low_prediction_{timestamp}.png')

        prepared_image_array = (prepared_image[0] * 255).astype(np.uint8)
        prepared_image_pil = Image.fromarray(prepared_image_array)
        # prepared_image_pil.save(image_path)

        return 'Не распознано'

    if predicted_class == 10: return '-'
    if predicted_class == 11: return 'x'

    result = predicted_class[0]

    return str(result)