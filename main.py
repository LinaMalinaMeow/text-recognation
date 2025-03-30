from mnist import mnist_model
from typed import typed
from table_recognize import table_recognize
import os
from PIL import Image
import shutil
from utils import utils

def get_table_info(path):
    row_results = []
    
    if os.path.exists('temp'):
        shutil.rmtree('temp')
    os.mkdir('temp')

    original_image_path = os.path.join('temp', 'original_image.jpg')
    image = Image.open(path)
    image.convert('RGB').save(original_image_path, format='JPEG')

    rows = table_recognize.run(path)

    for rowIndex, row in enumerate(rows):
        current_row_result = []
        for cellIndex, cell in enumerate(row):
            cropped_image = image.crop(cell)
            cropped_image_path = f'temp/cell_{rowIndex}_{cellIndex}.jpg'
            cropped_image.convert('RGB').save(cropped_image_path, format='JPEG')
            isEmpty = utils.is_cell_empty(cropped_image_path)

            if (isEmpty):
                current_row_result.append(' ')
                continue

            if (rowIndex % 2 == 0 or cellIndex == 0):
                extracted = typed.run(cropped_image_path)
            else:
                extracted = mnist_model.run(cropped_image_path)
                
            current_row_result.append(extracted.replace('\n', ' ').strip())
        
        row_results.append(current_row_result)
    
    return row_results

rows2 = get_table_info('test.jpg')

for row in rows2:
    print(row)
