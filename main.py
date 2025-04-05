import os
import shutil
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from io import BytesIO
from mnist import mnist_model
from table_recognize import table_recognize
from utils import utils
from pdf2image import convert_from_bytes
from ultralytics import YOLO

app = Flask(__name__)
CORS(app)

model = YOLO('preprocess_crop.pt')

def get_table_info(image):
    row_results = []

    try:
        if os.path.exists('temp'):
            shutil.rmtree('temp')
        os.mkdir('temp')
    except Exception as e:
        print(f"Ошибка при работе с временной директорией: {e}")
        return row_results

    original_image_path = os.path.join('temp', 'original_image.jpg')
    image.convert('RGB').save(original_image_path, format='JPEG')

    rows = table_recognize.run(original_image_path)

    for rowIndex, row in enumerate(rows):
        current_row_result = []
        for cellIndex, cell in enumerate(row):
            cropped_image = image.crop(cell)

            try:
                results = model(cropped_image)
                boxes = results[0].boxes.xyxy
            except Exception as e:
                print(f"Ошибка в модели YOLO: {e}")
                continue

            if boxes is not None and boxes.nelement() > 0:
                for box in boxes:
                    try:
                        x_min, y_min, x_max, y_max = map(int, box)
                        cropped_image_preprocessed = cropped_image.crop((x_min, y_min, x_max, y_max))
                        cropped_image_path = f'temp/cell_{rowIndex}_{cellIndex}.jpg'
                        cropped_image_preprocessed.convert('RGB').save(cropped_image_path, format='JPEG')
                    except Exception as e:
                        print(f"Ошибка при обрезке изображения: {e}")
            else:
                try:
                    cropped_image_path = f'temp/cell_{rowIndex}_{cellIndex}.jpg'
                    cropped_image.convert('RGB').save(cropped_image_path, format='JPEG')
                except Exception as e:
                    print(f"Ошибка при сохранении оригинальной ячейки: {e}")
                    continue

            try:
                isEmpty = utils.is_cell_empty(cropped_image_path)
            except Exception as e:
                print(f"Ошибка проверки содержимого ячейки: {e}")
                continue

            if isEmpty:
                current_row_result.append(' ')
                continue

            try:
                if rowIndex % 2 == 0:
                    if cellIndex == 0:
                        extracted = 'Номер задания'
                    else:
                        extracted = str(cellIndex)
                else:
                    if cellIndex == 0:
                        extracted = 'Баллы'
                    else:
                        extracted = mnist_model.run(cropped_image_path)

                current_row_result.append(extracted.replace('\n', ' ').strip())
            except Exception as e:
                print(f"Ошибка при извлечении данных: {e}")

        row_results.append(current_row_result)

    return row_results


@app.route('/recognize', methods=['POST'])
def recognize():
    data = request.json
    if 'image_base64' not in data:
        return jsonify({'error': 'No image data provided'}), 400

    try:
        image_data = base64.b64decode(data['image_base64'])
        
        with BytesIO(image_data) as image_buffer:
            image = Image.open(image_buffer)
            image.convert("RGB").save('decoded.jpg')
            image.load()
    except Exception as e:
        return jsonify({'error': f'Invalid image data: {str(e)}'}), 400

    try:
        table_info = get_table_info(image)
    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

    response = jsonify({'table_info': table_info})
    response.headers.add("Content-Type", "application/json; charset=utf-8")
    return response


@app.route('/recognize-pdf', methods=['POST'])
def recognize_pdf():
    if 'pdf_file' not in request.files:
        return jsonify({'error': 'No PDF file provided'}), 400
    
    pdf_file = request.files['pdf_file']

    try:
        pdf_data = pdf_file.read()
        images = convert_from_bytes(pdf_data, dpi=300)
    except Exception as e:
        return jsonify({'error': f'Invalid PDF data: {str(e)}'}), 400

    table_infos = []
    for i, image in enumerate(images):
        try:
            table_info = get_table_info(image)
            table_infos.append({'page': i + 1, 'table_info': table_info})
        except Exception as e:
            table_infos.append({'page': i + 1, 'error': f'Error processing page {i + 1}: {str(e)}'})

    response = jsonify({'tables': table_infos})
    response.headers.add("Content-Type", "application/json; charset=utf-8")
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)