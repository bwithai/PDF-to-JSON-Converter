import json
import pytesseract
from pdf2image import convert_from_path


def extract_text_from_pdf(pdf_path, page_number):
    images = convert_from_path(pdf_path, first_page=page_number, last_page=page_number)
    image = images[0].convert('L')

    # Save the image
    image_path = 'output/extracted_image_for_colab.png'
    image.save(image_path)

    # Perform OCR to extract text
    text = pytesseract.image_to_string(image)

    # Clean up and format the extracted text
    lines = text.strip().split('\n')
    table_data = [line.strip() for line in lines if line.strip()]

    # Create a dictionary structure
    data = {
        'pdf_path': pdf_path,
        'page_number': page_number,
        'table': table_data
    }

    # Convert dictionary to JSON
    json_data = json.dumps(data, indent=4)
    json_output_path = 'output/img_data_output.json'
    with open(json_output_path, 'w') as json_file:
        json_file.write(json_data)

    return "Extraction successful"


def main():
    pdf_path = 'test.pdf'
    page_number = 1  # page 1 and 2 only because it's an image.

    extracted_text = extract_text_from_pdf(pdf_path, page_number)
    print(extracted_text)


if __name__ == '__main__':
    main()