from typed import run
import preprocess_image
import matplotlib.pyplot as plt
import os

path = 'typed/test_images/'
image_paths = []

test_images_files = os.listdir(path)
for name in test_images_files:
    image_paths.append(f'{path}{name}')

print(image_paths)

preprocesed_images = []

for i, image_path in enumerate(image_paths):
    print(image_path)
    preprocessed = preprocess_image.run(image_path)
    preprocesed_images.append(preprocessed)

    extracted_text = run(image_path)

    extract_result = """
    {} результат: \n
    {}
    """.format(i+1, extracted_text)
    print(extract_result)

for i, preprocessed_image in enumerate(preprocesed_images):
    plt.figure()
    plt.imshow(preprocessed_image, cmap='gray')
    plt.title(f'Preprocessed Image {i+1}')
    plt.axis('off')

plt.show()