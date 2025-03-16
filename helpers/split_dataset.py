import os
import shutil
import random

def split_dataset(input_dir, output_dir, train_ratio=0.7, test_ratio=0.15, val_ratio=0.15):
    all_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    
    random.shuffle(all_files)

    num_train = int(len(all_files) * train_ratio)
    num_test = int(len(all_files) * test_ratio)
    num_val = len(all_files) - num_train - num_test

    train_files = all_files[:num_train]
    test_files = all_files[num_train:num_train + num_test]
    val_files = all_files[num_train + num_test:]

    train_dir = os.path.join(output_dir, 'train')
    test_dir = os.path.join(output_dir, 'test')
    val_dir = os.path.join(output_dir, 'val')
    
    for directory in [train_dir, test_dir, val_dir]:
        os.makedirs(directory, exist_ok=True)
    
    for file in train_files:
        shutil.copy(os.path.join(input_dir, file), os.path.join(train_dir, file))

    for file in test_files:
        shutil.copy(os.path.join(input_dir, file), os.path.join(test_dir, file))

    for file in val_files:
        shutil.copy(os.path.join(input_dir, file), os.path.join(val_dir, file))
    
    print("Файлы успешно распределены по каталогам.")

input_directory = 'dataset/x'
output_directory = 'dataset/x_spl'
split_dataset(input_directory, output_directory, train_ratio=0.7, test_ratio=0.15, val_ratio=0.15)