import argparse
import os
from dotenv import load_dotenv

from pdf_to_json import PdfParser

load_dotenv()

# Set default values
default_pdf_path = "test.pdf"
default_pdf_context = "items"

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Convert PDF into JSON.")
parser.add_argument("--pdf-path", type=str, default=default_pdf_path, help="Path to the PDF file.")
parser.add_argument("--pdf-context", type=str, default=default_pdf_context, choices=["items", "img", "clauses"],
                    help="Specify the PDF context: 'items', 'img', or 'clauses'.")
# Items from 3 to 27 and clauses from 45 to 49
parser.add_argument("--start-page", type=int, help="Start page number for items or clauses.")
parser.add_argument("--end-page", type=int, help="End page number for items or clauses.")
args = parser.parse_args()

# Check if the PDF file exists
if not os.path.exists(args.pdf_path):
    print("Error: The specified PDF file does not exist.")
    exit(1)

# Initialize the PdfParser instance with API key and PDF context
api_key = os.getenv("OPENAI_API_KEY")
parser = PdfParser(api_key, args.pdf_context)

# Process PDF based on the specified context
if args.pdf_context == "items" or args.pdf_context == "clauses":
    """
        if you found estimated_answer_tokens lower than max_tokens, changing max_tokens to 857
        reduce the number of pages. OpenAI token exceed
    """
    if args.start_page is None or args.end_page is None:
        print("Error: Start page and end page must be specified for 'items' or 'clauses' context.")
        exit(1)

    # Convert PDF pages to string
    pdf_str = parser.convert_pdf_to_string(args.pdf_path, args.start_page, args.end_page, args.pdf_context)

    # Query the PDF content
    query = parser.query_pdf(pdf_str)
    print(query)

elif args.pdf_context == "img":
    page_number = 1  # Process only page 1 and 2 since it's an image-based PDF
    parser.extract_text_from_ImgPdf(args.pdf_path, page_number)
