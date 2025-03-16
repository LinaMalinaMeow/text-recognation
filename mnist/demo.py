import numpy as np
from keras import models
from keras import datasets
import matplotlib.pyplot as plt
import mnist_model

model = models.load_model('mnist/mnist_recognation_extendend.h5')

def mnist_test_data_demo():
    (_, _), (x_test, y_test) = datasets.mnist.load_data()
    x_test = x_test.astype('float32') / 255
    x_test = np.expand_dims(x_test, -1)

    predictions = model.predict(x_test)

    predicted_classes = np.argmax(predictions, axis=1)

    print(f"Предсказанные классы для первых 10 тестовых изображений: {predicted_classes[:10]}")
    print(f"Правильные классы для первых 10 тестовых изображений: {y_test[:10]}")

    plt.imshow(x_test[0].reshape(28, 28), cmap='gray')
    plt.title(f"Предсказанный класс: {predicted_classes[0]}")
    plt.show()

def custom_data_demo():
    def get_path(filename):
        return f'mnist/test_images/{filename}'

    result1 = mnist_model.mnist_recognation(get_path('test1.png'))
    result2 = mnist_model.mnist_recognation(get_path('test2.png'))
    result3 = mnist_model.mnist_recognation(get_path('test3_negative.png'))
    result4 = mnist_model.mnist_recognation(get_path('test4_negative.png'))
    result5 = mnist_model.mnist_recognation(get_path('test5_very_negative.png'))
    result6 = mnist_model.mnist_recognation(get_path('test6_cross.png'))
    result7 = mnist_model.mnist_recognation(get_path('test7_dash.png'))

    print(f'Результат 1 должен быть равен 1, равен - {result1}')
    print(f'Результат 2 должен быть равен 2, равен - {result2}')
    print(f'Результат 3 (без препроцессинга не определяет) должен быть равен 2, равен - {result3}')
    print(f'Результат 4 (перечеркнутая единица) должен быть равен 1, равен - {result4}')
    print(f'Результат 5 (очень непонятная двойка) должен быть равен 2, равен - {result5}')
    print(f'Результат 6 (крестик), равен - {result6}')
    print(f'Результат 7 (прочерк), равен - {result7}')

custom_data_demo()