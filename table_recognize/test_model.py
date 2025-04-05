from table_recognize import run
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

base_path = 'table_recognize/test_images'

coordinates_results = [
    run(f'{base_path}/test_image1.jpg'),
    run(f'{base_path}/test_image3.png'),
    run(f'{base_path}/image2.jpg'),
    run(f'{base_path}/test_image4.jpg'),
    run(f'{base_path}/image3.png')
]

image_paths = [
    f'{base_path}/test_image1.jpg',
    f'{base_path}/test_image3.png',
    f'{base_path}/image2.jpg',
    f'{base_path}/test_image4.jpg',
    f'{base_path}/image3.png'
]

for image_path, coordinates in zip(image_paths, coordinates_results):
    image = Image.open(image_path)
    
    num_rows = len(coordinates)
    num_columns = max(len(row) for row in coordinates)
    
    fig, axs = plt.subplots(num_rows, num_columns, figsize=(15, 10))
    
    axs = axs if isinstance(axs, (list, np.ndarray)) else [[axs]]
    
    for row_idx, row in enumerate(coordinates):
        for col_idx, (x1, y1, x2, y2) in enumerate(row):
            cell_img = image.crop((x1, y1, x2, y2))
            
            axs[row_idx][col_idx].imshow(cell_img)
            axs[row_idx][col_idx].axis('off')
    
    for row_idx in range(num_rows):
        for col_idx in range(num_columns):
            if col_idx >= len(coordinates[row_idx]):
                axs[row_idx][col_idx].axis('off')
    
    plt.tight_layout()
    plt.show()