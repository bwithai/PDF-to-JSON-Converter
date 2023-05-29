import pdftotext
import openai
import re
import logging
import json
from pdf2image import convert_from_path
from pytesseract import pytesseract

from prompt import prompt_items, prompt_clauses


class PdfParser:
    def __init__(self, openai_api_key, context):
        if context == "items":
            self.prompt_questions = prompt_items
        elif context == "clauses":
            self.prompt_questions = prompt_clauses
        else:
            print("please specify the context in the form of 'items' or 'img' or 'clauses'")
        openai.api_key = openai_api_key
        self.logger = logging.getLogger(__name__)

    def convert_pdf_to_string(self, pdf_path, start_page, end_page, context):
        with open(pdf_path, "rb") as f:
            pdf = pdftotext.PDF(f)
            if context == "clauses":
                page_text = pdf[start_page - 1]
            elif context == "items":
                page_text = [pdf[page_num - 1] for page_num in range(start_page, end_page + 1)]

        pdf_str = "\n\n".join(page_text)
        pdf_str = re.sub('\s[,.]', ',', pdf_str)
        pdf_str = re.sub('[\n]+', '\n', pdf_str)
        pdf_str = re.sub('[\s]+', ' ', pdf_str)
        pdf_str = re.sub('http[s]?(://)?', '', pdf_str)

        return pdf_str

    def query_completion(self, prompt, engine='text-curie-001', temperature=0.0, max_tokens=100, top_p=1,
                         frequency_penalty=0, presence_penalty=0):
        self.logger.info(f'query_completion: using {engine}')
        estimated_prompt_tokens = int(len(prompt.split()) * 1.6)
        self.logger.info(f'estimated prompt tokens: {estimated_prompt_tokens}')
        estimated_answer_tokens = 2049 - estimated_prompt_tokens
        if estimated_answer_tokens < max_tokens:
            self.logger.warning('estimated_answer_tokens lower than max_tokens, changing max_tokens to %d',
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

    def query_pdf(self, pdf_str):
        print("Query begin to parse pdf into organize structure")
        self.logger.debug(pdf_str)
        prompt = f"{self.prompt_questions}\n{pdf_str}"
        max_tokens = 1500
        engine = 'text-davinci-002'
        response = self.query_completion(prompt, engine=engine, max_tokens=max_tokens)
        response_text = response['choices'][0]['text'].strip()
        self.logger.debug(response_text)
        output_path = "output/result.json"
        try:
            pdf = json.loads(response_text)
            with open(output_path, 'w') as json_file:
                json.dump(pdf, json_file, indent=4)
            self.logger.info(f"Json file save to {output_path}")
        except json.decoder.JSONDecodeError as e:
            self.logger.error('Error decoding JSON: %s', e)
            print('Failed to parse the pdf. Please check the log for details.')
        return response_text

    def extract_text_from_ImgPdf(self, pdf_path, page_number):
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
