import io

import pymupdf  # PyMuPDF library
from PIL import Image


def images_to_pdf(image_bytes_list):
    """
    Convert multiple images to single PDF

    Args:
        image_bytes_list: List of image bytes objects

    Returns:
        BytesIO object containing PDF
    """
    # Create new PDF
    pdf_doc = pymupdf.open()

    for img_bytes in image_bytes_list:
        # Open image
        img_doc = pymupdf.open(stream=img_bytes, filetype="png")
        rect = img_doc[0].rect

        # Convert to PDF
        pdf_bytes = img_doc.convert_to_pdf()
        img_doc.close()

        # Add as new page
        img_pdf = pymupdf.open("pdf", pdf_bytes)
        page = pdf_doc.new_page(width=rect.width, height=rect.height)
        page.show_pdf_page(rect, img_pdf, 0)

    # Export
    output = io.BytesIO()
    output.write(pdf_doc.tobytes())
    output.seek(0)

    pdf_doc.close()
    return output
