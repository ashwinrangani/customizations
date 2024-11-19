import frappe

from PIL import Image
import pytesseract
from werkzeug.utils import secure_filename
import os

@frappe.whitelist(allow_guest=True)
def process_scanned_document():
    uploaded_file = frappe.request.files.get('file')
    if not uploaded_file:
        frappe.throw("No file uploaded.")

    # Save the uploaded file temporarily
    file_path = os.path.join('/tmp', secure_filename(uploaded_file.filename))
    uploaded_file.save(file_path)

    try:
        # If the file is an image, process it directly
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            text = pytesseract.image_to_string(Image.open(file_path))
        elif file_path.lower().endswith('.pdf'):
            frappe.throw("PDF OCR processing requires additional tools. Convert to an image first.")
        else:
            frappe.throw("Unsupported file format.")

        # Example: Parse the text to extract fields
        invoice_data = extract_invoice_data(text)

        return invoice_data

    except Exception as e:
        frappe.log_error(f"Error processing document: {str(e)}")
        frappe.throw("Failed to process the document.")
    finally:
        # Clean up temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

def extract_invoice_data(text):
    # Example: Parse text using simple string matching or regex
    lines = text.split('\n')
    invoice_data = {
        "supplier": find_value_in_lines(lines, "Supplier"),
        "invoice_number": find_value_in_lines(lines, "Invoice Number"),
        "date": find_value_in_lines(lines, "Date"),
        "total_amount": find_value_in_lines(lines, "Total"),
    }
    return invoice_data

def find_value_in_lines(lines, key):
    for line in lines:
        if key.lower() in line.lower():
            return line.split(':')[-1].strip()
    return None
