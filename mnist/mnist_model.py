from keras import models
import numpy as np
import sys
import os
# todo: сделать нормально
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared import mnist_preprocess

# Вычислено эмпирическим путем
MAX_RECOGNATION_PERCENT = 0.45


def run(path):
    prepared_image = mnist_preprocess.rec_digit(path)

    model = models.load_model('mnist/mnist_recognation_extendend.h5')

    prediction = model.predict(prepared_image)

    max_predict = np.amax((prediction[0]))
    print(prediction)

    if (max_predict < MAX_RECOGNATION_PERCENT):
        return 'Не распознано'

    predicted_class = np.argmax(prediction, axis=1)

    if (predicted_class == 10): return '-'
    if (predicted_class == 11): return 'x'

    result = predicted_class[0]

    return str(result)