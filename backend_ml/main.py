import os
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from io import BytesIO
from mnist import mnist_model
from table_recognize import table_recognize
from utils import utils
import io
import fitz
import cv2
import numpy as np
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder='static')
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

socketio = SocketIO(app, cors_allowed_origins="*")

def get_table_info(image, page_number):
    row_results = []

    page_dir = f'temp/{page_number}'
    os.makedirs(page_dir, exist_ok=True)

    original_image_path = os.path.join(page_dir, 'original_image.png')
    image.save(original_image_path)

    try:
        rows = table_recognize.run(image)
        for rowIndex, row in enumerate(rows):
            current_row_result = []
            for cellIndex, cell in enumerate(row):
                cropped_image = image.crop(cell)

                cell_path = os.path.join(page_dir, f'cell_{rowIndex}_{cellIndex}.png')
                cropped_image.save(cell_path)

                try:
                    isEmpty = utils.is_cell_empty(cropped_image)
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
                            extracted = mnist_model.run(cropped_image)

                    current_row_result.append(extracted.replace('\n', ' ').strip())
                except Exception as e:
                    print(f"Ошибка при извлечении данных: {e}")

            row_results.append(current_row_result)
    except Exception as e:
        print(f"Ошибка при обработке таблицы: {e}")

    return row_results



@app.route('/recognize', methods=['POST'])
def recognize():
    data = request.json
    if 'image_base64' not in data:
        return jsonify({'error': 'No image data provided'}), 400

    try:
        image_data = base64.b64decode(data['image_base64'])
        with BytesIO(image_data) as image_buffer:
            image = Image.open(image_buffer).convert("RGB")
    except Exception as e:
        return jsonify({'error': f'Invalid image data: {str(e)}'}), 400

    try:
        table_info = get_table_info(image)
    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500

    response = jsonify({'table_info': table_info})
    response.headers.add("Content-Type", "application/json; charset=utf-8")
    return response


def preprocess_image(image: Image):
    image_np = np.array(image)

    gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

    height, width = gray_image.shape
    upscale_factor = 2
    enlarged_image = cv2.resize(gray_image, (upscale_factor * width, upscale_factor * height), interpolation=cv2.INTER_CUBIC)

    blurred_image = cv2.GaussianBlur(enlarged_image, (5, 5), 0)

    denoised_image = cv2.fastNlMeansDenoising(blurred_image, h=30)

    sharpening_kernel = np.array([[-1, -1, -1], 
                                  [-1,  9, -1],
                                  [-1, -1, -1]])
    sharpened_image = cv2.filter2D(denoised_image, -1, sharpening_kernel)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    equalized_image = clahe.apply(sharpened_image)

    final_image = cv2.cvtColor(equalized_image, cv2.COLOR_GRAY2RGB)

    preprocessed_image = Image.fromarray(final_image)
    return preprocessed_image

@app.route('/recognize-pdf', methods=['POST'])
def recognize_pdf():
    if 'pdf_file' not in request.files:
        return jsonify({'error': 'Не предоставлен PDF-файл'}), 400

    pdf_file = request.files['pdf_file']

    try:
        pdf_data = pdf_file.read()
        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
    except Exception as e:
        return jsonify({'error': f'Неверные данные PDF: {str(e)}'}), 400

    table_infos = []
    output_dir = 'static/pdf_pages'
    preprocessed_output_dir = 'static/pdf_pages/preprocessed'
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(preprocessed_output_dir, exist_ok=True)

    for i in range(len(pdf_document)):
        try:
            page = pdf_document.load_page(i)
            pix = page.get_pixmap(dpi=300)
            image_bytes = pix.tobytes("png")

            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')

            original_image_filename = f'page_{i + 1}.png'
            original_image_path = os.path.join(output_dir, original_image_filename)
            image.save(original_image_path, format='PNG')

            preprocessed_image = preprocess_image(image)

            preprocessed_image_filename = f'page_{i + 1}_preprocessed.png'
            preprocessed_image_path = os.path.join(preprocessed_output_dir, preprocessed_image_filename)
            preprocessed_image.save(preprocessed_image_path, format='PNG')

            table_info = get_table_info(preprocessed_image, i+1)
            print(table_info)

            table_infos.append({
                'page': i + 1,
                'table_info': table_info,
                'image_url': f'/static/pdf_pages/{original_image_filename}',
            })
        except Exception as e:
            table_infos.append({
                'page': i + 1,
                'error': f'Ошибка при обработке страницы {i + 1}: {str(e)}',
                'image_url': None,
            })

    response = jsonify({'tables': table_infos})
    response.headers.add("Content-Type", "application/json; charset=utf-8")
    return response

@app.route('/recognize-pdf-socket', methods=['POST'])
def recognize_pdf_socket():
    socketio.emit('pdf_status', {"is_loading": True})

    if 'pdf_file' not in request.files:
        return jsonify({'error': 'Не предоставлен PDF-файл'}), 400

    pdf_file = request.files['pdf_file']

    try:
        pdf_data = pdf_file.read()
        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
    except Exception as e:
        return jsonify({'error': f'Неверные данные PDF: {str(e)}'}), 400
    

    output_dir = 'static/pdf_pages'
    preprocessed_output_dir = 'static/pdf_pages/preprocessed'
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(preprocessed_output_dir, exist_ok=True)

    for i in range(len(pdf_document)):
        try:
            page = pdf_document.load_page(i)
            pix = page.get_pixmap(dpi=300)
            image_bytes = pix.tobytes("png")

            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')

            original_image_filename = f'page_{i + 1}.png'
            original_image_path = os.path.join(output_dir, original_image_filename)
            image.save(original_image_path, format='PNG')

            preprocessed_image = preprocess_image(image)

            preprocessed_image_filename = f'page_{i + 1}_preprocessed.png'
            preprocessed_image_path = os.path.join(preprocessed_output_dir, preprocessed_image_filename)
            preprocessed_image.save(preprocessed_image_path, format='PNG')

            table_info = get_table_info(preprocessed_image, i + 1)

            socketio.emit('pdf_status', {"is_loading": False})
            socketio.emit('page_processed', {
                'page': i + 1,
                'table_info': table_info,
                'image_url': f'/static/pdf_pages/{original_image_filename}',
            })
        except Exception as e:
            socketio.emit('page_processed', {
                'page': i + 1,
                'error': f'Ошибка при обработке страницы {i + 1}: {str(e)}',
                'image_url': None,
            })

    return jsonify({'message': 'PDF обработан'}), 200


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5001)
