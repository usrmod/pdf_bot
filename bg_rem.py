import io

from rembg import remove


def rem_image(bytes):
    output_bytes = remove(bytes)

    output_image = io.BytesIO(output_bytes)
    output_image.seek(0)

    return output_image
