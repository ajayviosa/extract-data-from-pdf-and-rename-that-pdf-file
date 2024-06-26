import os
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import re

# Add poppler bin directory to the system PATH
poppler_path = r'C:\poppler-24.02.0\Library\bin'  # Replace with the actual path to your poppler's bin directory
if poppler_path not in os.environ['PATH']:
    os.environ['PATH'] += os.pathsep + poppler_path

# Specify the exact path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to extract text from an image-based PDF
def extract_text_from_image_based_pdf(pdf_path):
    # print("System PATH:", os.environ['PATH'])
    
    try:
        pages = convert_from_path(pdf_path)
    except Exception as e:
        print(f"Error converting PDF: {e}")
        return ""
    
    text = ""
    for page in pages:
        text += pytesseract.image_to_string(page)
    return text

# Function to extract the name from the text
def extract_name(text):
    match = re.search(r"Name\s*:\s*([\w\s]+)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

# Function to rename the PDF
def rename_pdf(pdf_path, new_name):
    directory = os.path.dirname(pdf_path)
    sanitized_name = "".join([c if c.isalnum() else "_" for c in new_name])  # Sanitize the file name
    new_path = os.path.join(directory, f"{sanitized_name}.pdf")
    os.rename(pdf_path, new_path)
    return new_path

# Function to process all PDFs in a folder
def process_pdfs_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            text = extract_text_from_image_based_pdf(pdf_path)
            name = extract_name(text)
            if name:
                new_pdf_path = rename_pdf(pdf_path, name)
                print(f"PDF '{filename}' renamed to '{os.path.basename(new_pdf_path)}'")
            else:
                print(f"Name not found in '{filename}'")

# Example usage
folder_path = r'D:\Ajay - Viosa\extract data from pdf'  # Replace with the actual path to your folder
process_pdfs_in_folder(folder_path)
