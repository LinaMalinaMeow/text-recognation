import preprocess_image
import pytesseract

def get_text_from_image(image_path):
    processed_image = preprocess_image.run(image_path)
    extracted_text = pytesseract.image_to_string(processed_image, lang='rus')

    return extracted_text