import shutil
import os
import io

from PIL import Image

def move_file_to_downloads(file_path):
    downloads_path = os.path.expanduser('~/Downloads/')
    
    file_name = os.path.basename(file_path)
    destination = os.path.join(downloads_path, file_name)
    
    try:
        shutil.move(file_path, destination)
        print(f"File moved to {destination}")
    except Exception as e:
        print(f"Error moving file: {e}")


def downsample_image(image_bytes: bytes) -> bytes:
    original_image = Image.open(io.BytesIO(image_bytes))
    
    resized_image = original_image.resize((128, 128))
    
    output = io.BytesIO()
    resized_image.save(output, format='JPEG')
    downsized_image_bytes = output.getvalue()
    
    return downsized_image_bytes



