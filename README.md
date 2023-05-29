# PDF to JSON Converter

This is a Python script that converts PDF files into JSON format. It provides options to extract specific information such as items, clauses, or perform OCR on image-based PDFs.

## Prerequisites

- Python 3.10 or above
- `pip` package manager
- Tesseract OCR (for image-based PDF extraction)

## Installation

1. Clone the repository or download the source code.

2. Install the required dependencies by running the following command:

   ```bash
   pip install -r build/requirements.txt
3. If you're planning to extract text from image-based PDFs, make sure Tesseract OCR is installed on your system. You can find installation instructions for your operating system in the Tesseract OCR documentation.
4. Set up your OpenAI API key by creating a .env file in the project directory and adding the following line:
   `OPENAI_API_KEY=your_api_key_here` Replace your_api_key_here with your actual OpenAI API key.

## Usage

1. Run the script with the following command:
   ```bash
   python main.py --pdf-path <path-to-pdf> --pdf-context <context> --start-page <start-page> --end-page <end-page>
2. Replace `path/to/your/pdf_file.pdf` with the path to your PDF file. Adjust the `pdf-context` argument according to your requirements (`items`, `img`, or `clauses`). If extracting items or clauses, specify the start-page and end-page arguments accordingly.

3. The script will convert the PDF file to JSON and print the extracted information or perform OCR on image-based PDFs.

## Options
The script accepts the following command-line options:

- `--pdf-path`: Path to the PDF file.
- `--pdf-context`: Specify the PDF context: items, img, or clauses.
- `--start-page`: Start page number for items or clauses (required for items and clauses context).
- `--end-page`: End page number for items or clauses (required for items and clauses context).