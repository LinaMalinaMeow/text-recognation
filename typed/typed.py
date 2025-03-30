import easyocr

def run(image_path):
    reader = easyocr.Reader(['ru', 'en'])

    result = reader.readtext(image_path)

    extracted_text = ' '.join([detection[1] for detection in result])

    return extracted_text
