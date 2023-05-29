import json
import logging
import os
import re

import openai
import pdftotext
from pdf2image import convert_from_path
from pytesseract import pytesseract

from prompt import PROMPT_ITEMS

LOGGER = logging.getLogger(__name__)


def convert_pdf_to_string(pdf_path, start_page, end_page):
    with open(pdf_path, "rb") as f:
        pdf = pdftotext.PDF(f)
        page_text = [pdf[page_num - 1] for page_num in range(start_page, end_page + 1)]

    # Join the elements of page_text with double line breaks
    pdf_str = "\n\n".join(page_text)

    # Replace spaces followed by commas or periods with commas
    pdf_str = re.sub('\s[,.]', ',', pdf_str)

    # Replace multiple consecutive newline characters with a single newline character
    pdf_str = re.sub('[\n]+', '\n', pdf_str)

    # Replace multiple consecutive whitespace characters with a single space
    pdf_str = re.sub('[\s]+', ' ', pdf_str)

    # Remove occurrences of URLs (http://, https://, http:/, https:/)
    pdf_str = re.sub('http[s]?(://)?', '', pdf_str)

    return pdf_str


def extract_text_from_image_pdf(pdf_path, page_number):
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

    return "Img convert to json successfully"


def query_completion(prompt, engine='text-curie-001', temperature=0.0, max_tokens=100, top_p=1,
                     frequency_penalty=0, presence_penalty=0):
    LOGGER.info(f'query_completion: using {engine}')
    estimated_prompt_tokens = int(len(prompt.split()) * 1.6)
    LOGGER.info(f'estimated prompt tokens: {estimated_prompt_tokens}')
    estimated_answer_tokens = 2049 - estimated_prompt_tokens
    if estimated_answer_tokens < max_tokens:
        LOGGER.warning('estimated_answer_tokens lower than max_tokens, changing max_tokens to %d',
                       estimated_answer_tokens)
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temperature,
        max_tokens=min(4097 - estimated_prompt_tokens, max_tokens),
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )
    return response


class PdfParser:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY", None)
        if api_key is None:
            LOGGER.warning(f"OPENAI_API_KEY does not exists in the .env file. Please set that first to proceed.")
            exit(1)
        self.prompt_items = PROMPT_ITEMS
        openai.api_key = api_key

    def query_pdf(self, pdf_str):
        print("Query begin to parse pdf into organize structure")
        LOGGER.debug(pdf_str)
        prompt = f"{self.prompt_items}\n{pdf_str}"
        max_tokens = 1500
        engine = 'text-davinci-002'
        response = query_completion(prompt, engine=engine, max_tokens=max_tokens)
        response_text = response['choices'][0]['text'].strip()
        LOGGER.debug(response_text)
        output_path = "output/result.json"
        try:
            pdf = json.loads(response_text)
            with open(output_path, 'w') as json_file:
                json.dump(pdf, json_file, indent=4)
            LOGGER.info(f"Json file save to {output_path}")
        except json.decoder.JSONDecodeError as e:
            LOGGER.error('Error decoding JSON: %s', e)
            print('Failed to parse the pdf. Please check the log for details.')
        return response_text
