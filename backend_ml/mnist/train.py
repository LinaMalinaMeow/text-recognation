import os
import numpy as np
import keras
from keras import layers
from keras import regularizers
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

datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1. / 255,
)

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

# model = keras.Sequential([
#     keras.Input(shape=input_shape),
#     layers.Conv2D(32, kernel_size=(3, 3), activation="relu", kernel_regularizer=regularizers.L2(0.001)),
#     layers.BatchNormalization(),
#     layers.MaxPooling2D(pool_size=(2, 2)),
#     layers.Conv2D(64, kernel_size=(3, 3), activation="relu", kernel_regularizer=regularizers.L2(0.001)),
#     layers.BatchNormalization(),
#     layers.MaxPooling2D(pool_size=(2, 2)),
#     layers.Conv2D(128, kernel_size=(3, 3), activation="relu", kernel_regularizer=regularizers.L2(0.001)),
#     layers.BatchNormalization(),
#     layers.MaxPooling2D(pool_size=(2, 2)),
#     layers.Flatten(),
#     layers.Dropout(0.5),
#     layers.Dense(128, activation="relu", kernel_regularizer=regularizers.L2(0.001)),
#     layers.Dropout(0.5),
#     layers.Dense(num_classes, activation="softmax"),
# ])

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
epochs = 100

def count_files(directory):
    return sum([len(files) for _, _, files in os.walk(directory)])

nb_train_samples = count_files('dataset/train')
nb_val_samples = count_files('dataset/val')
nb_test_samples = count_files('dataset/test')

model.compile(
    loss="categorical_crossentropy",
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    metrics=["accuracy"]
)

callbacks = [
    tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
    tf.keras.callbacks.ModelCheckpoint(filepath='mnist/best_model_test1.h5', monitor='val_loss', save_best_only=True)
]

model.fit(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=val_generator,
    validation_steps=nb_val_samples // batch_size,
    callbacks=callbacks
)

model.load_weights('mnist/best_model_test1.h5')

scores = model.evaluate(test_generator, steps=nb_test_samples // batch_size)

print("Test loss:", scores[0])
print("Test accuracy:", scores[1])