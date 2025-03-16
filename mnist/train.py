import numpy as np
import keras
from keras import layers
import ssl
import requests
import tensorflow as tf

requests.packages.urllib3.disable_warnings()

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

num_classes = 12
input_shape = (28, 28, 1)

datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1. / 255)

train_generator = datagen.flow_from_directory(
    'dataset/train',
    target_size=(28, 28),
    batch_size=128,
    class_mode='categorical',
    color_mode='grayscale'
)

val_generator = datagen.flow_from_directory(
    'dataset/val',
    target_size=(28, 28),
    batch_size=128,
    class_mode='categorical',
    color_mode='grayscale'
)

test_generator = datagen.flow_from_directory(
    'dataset/test',
    target_size=(28, 28),
    batch_size=128,
    class_mode='categorical',
    color_mode='grayscale'
)

model = keras.Sequential(
    [
        keras.Input(shape=input_shape),
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation="softmax"),
    ]
)

batch_size = 128
epochs = 15
nb_test_samples = 10944
nb_train_samples = 51096

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

model.fit(
    train_generator,
    batch_size=batch_size,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=val_generator,
    validation_split=0.1
)

scores = model.evaluate(
    test_generator, 
    steps=nb_test_samples // batch_size
)

model.save('mnist/mnist_recognation_extendend.h5')

print("Test loss:", scores[0])
print("Test accuracy:", scores[1])
