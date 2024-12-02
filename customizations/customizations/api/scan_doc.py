import frappe
import os
from werkzeug.utils import secure_filename

@frappe.whitelist()
def process_doc():
    # Access the uploaded file
    uploaded_file = frappe.request.files.get('file')  # Get file from request
    if not uploaded_file:
        frappe.throw("No file uploaded.")

    # Save the file temporarily
    file_path = os.path.join('/tmp', secure_filename(uploaded_file.filename))
    uploaded_file.save(file_path)

    # Dummy OCR processing or file handling
    try:
        frappe.logger().debug(f"Processing file: {file_path}")
        # Add your OCR or file processing logic here
        # Example return data:
        return {
            "supplier": "Desire Wholesalers",
            "invoice_number": "INV12345",
            "date": "2024-11-19",
            "total_amount": 1234.56,
        }
    except Exception as e:
        frappe.throw(f"Error processing file: {str(e)}")
    finally:
        # Clean up temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
