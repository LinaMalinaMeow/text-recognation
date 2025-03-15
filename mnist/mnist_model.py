from keras import models
import numpy as np
import mnist_preprocess

# Вычислено эмпирическим путем
MAX_RECOGNATION_PERCENT = 0.7

def show_procentages(prediction):
    percentages = prediction * 100
    classes = range(9)
    for cls, pct in zip(classes, percentages[0]):
        print(f"Класс {cls}: {pct:.2f}%")

def mnist_recognation(path):
    prepared_image = mnist_preprocess.rec_digit(path)

    model = models.load_model('mnist/mnist_recognation.h5')

    prediction = model.predict(prepared_image)
    show_procentages(prediction)

    max_predict = np.amax((prediction[0]))

    if (max_predict < MAX_RECOGNATION_PERCENT):
        return 'Пропуск'

    predicted_class = np.argmax(prediction, axis=1)
    result = predicted_class[0]

    return result