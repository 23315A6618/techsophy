import os
from PIL import Image
import fitz  

def is_supported_file(filename):
    """Check if file is a supported document/image type."""
    supported_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.tiff']
    ext = os.path.splitext(filename)[1].lower()
    return ext in supported_extensions

def pdf_to_images(pdf_path):
    """
    Convert each page of PDF to a PIL Image.
    Returns list of images.
    """
    images = []
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombyte
