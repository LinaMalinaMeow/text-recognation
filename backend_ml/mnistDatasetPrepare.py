import os
import cv2
import numpy as np
from albumentations import Compose, Rotate, GaussNoise, RandomBrightnessContrast, ShiftScaleRotate

def augment_images_to_target_per_folder(base_folder):
    transform = Compose([
        Rotate(limit=10, p=0.5),
        GaussNoise(p=0.5),
        RandomBrightnessContrast(p=0.5),
        ShiftScaleRotate(shift_limit=0.1, scale_limit=0.1, rotate_limit=10, p=0.5)
    ])

    max_count = 0
    folders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]
    folder_paths = [os.path.join(base_folder, folder) for folder in folders]
    
    for folder_path in folder_paths:
        image_count = len(os.listdir(folder_path))
        max_count = max(max_count, image_count)
    
    print(f"Максимальное количество изображений в одной из папок: {max_count}")

    for folder_path in folder_paths:
        images_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        image_count = len(images_files)
        
        if image_count < max_count:
            images = [cv2.imread(os.path.join(folder_path, f)) for f in images_files if cv2.imread(os.path.join(folder_path, f)) is not None]
            
            while image_count < max_count:
                to_generate = min(max_count - image_count, len(images))
                images_to_augment = images[:to_generate]

                for img in images_to_augment:
                    augmented = transform(image=img)["image"]
                    new_filename = f"aug_{image_count}.png"
                    cv2.imwrite(os.path.join(folder_path, new_filename), augmented)
                    image_count += 1

                print(f"Папка {os.path.basename(folder_path)}: добавлено {to_generate} изображений. Всего сейчас: {image_count}/{max_count}")

augment_images_to_target_per_folder('./dataset/val')