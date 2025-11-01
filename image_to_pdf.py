import io

import pymupdf  # PyMuPDF library
from PIL import Image

# Constant A4 dimentions for pdf
WIDTH_A4 = 1238
HEIGHT_A4 = 1754


def single_image_to_pdf(image_bytes):
    new_pdf_doc = pymupdf.open()

    image_from_bytes = pymupdf.open(stream=image_bytes, filetype="png")

    image_dimentions = image_from_bytes[0].rect

    pdf_bytes = image_from_bytes.convert_to_pdf()
    image_from_bytes.close()

    image_pdf = pymupdf.open("pdf", pdf_bytes)

    page = new_pdf_doc.new_page(
        width=image_dimentions.width, height=image_dimentions.height
    )
    page.show_pdf_page(image_dimentions, image_pdf, 0)

    # Save to BytesIO
    output = io.BytesIO()
    output.write(new_pdf_doc.tobytes())
    output.seek(0)

    new_pdf_doc.close()
    return output


def images_to_pdf(image_bytes_list):
    """
    Convert multiple images to single multi-page PDF

    Args:
        image_bytes_list: List of image bytes (in order)

    Returns:
        BytesIO object containing PDF
    """
    # Create new PDF document
    pdf_doc = pymupdf.open()

    # Process each image
    for img_bytes in image_bytes_list:
        # Open image from bytes
        img_doc = Image.open(io.BytesIO(img_bytes))
        img_width = img_doc.width
        img_height = img_doc.height
        # img_doc = pymupdf.open(stream=img_bytes, filetype="png")
        # dimentions = img_doc[0].rect

        # Create A4 with white blank background
        page = pdf_doc.new_page(width=WIDTH_A4, height=HEIGHT_A4)

        # # Convert image to PDF format
        # pdf_bytes = img_doc.convert_to_pdf()
        # img_doc.close()

        # # Add as new page to main document
        # img_pdf = pymupdf.open("pdf", pdf_bytes)
        # page.show_pdf_page(dimentions, img_pdf, 0)

        target_rect = fit_image_to_page(img_width, img_height, WIDTH_A4, HEIGHT_A4)

        # Insert image at calculated position
        # page.show_pdf_page(target_rect, img_pdf, 0)
        page.insert_image(target_rect, stream=img_bytes)

    # Export to BytesIO
    output = io.BytesIO()
    output.write(pdf_doc.tobytes())
    output.seek(0)

    pdf_doc.close()
    return output


def fit_image_to_page(img_width, img_height, page_width, page_height, margin=0):
    """
    Calculate rectangle to fit image in page while maintaining aspect ratio

    Args:
        img_rect: Original image rectangle (has .width and .height)
        page_width: Target page width
        page_height: Target page height
        margin: Margin around image (in points)

    Returns:
        pymupdf.Rect with calculated position and size
    """
    # Available space (page size minus margins)
    available_width = page_width - (2 * margin)
    available_height = page_height - (2 * margin)

    # # Original image dimensions
    # img_width = img_rect.width
    # img_height = img_rect.height

    # Calculate scaling ratios
    width_ratio = available_width / img_width
    height_ratio = available_height / img_height

    # Use smaller ratio to ensure image fits entirely
    scale = min(width_ratio, height_ratio)

    # Calculate new dimensions
    new_width = img_width * scale
    new_height = img_height * scale

    # Center the image on page
    x0 = (page_width - new_width) / 2
    y0 = (page_height - new_height) / 2
    x1 = x0 + new_width
    y1 = y0 + new_height

    # Return rectangle with calculated position
    return pymupdf.Rect(x0, y0, x1, y1)
