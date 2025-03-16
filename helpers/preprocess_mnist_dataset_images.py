import sys
import os
from PIL import Image
import numpy as np
# todo: сделать нормально
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared.mnist_preprocess import rec_digit

def process_and_save_images(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        
        if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            processed_img = rec_digit(file_path)

            processed_img = np.squeeze(processed_img)
            processed_img *= 255.0
            processed_img = processed_img.astype(np.uint8)

            img = Image.fromarray(processed_img)

            result_path = os.path.join(output_dir, filename)
            img.save(result_path)

    print("Успешно")

input_directory = 'dataset/train/0'
output_directory = 'dataset/train/0_n'

process_and_save_images(input_directory, output_directory)