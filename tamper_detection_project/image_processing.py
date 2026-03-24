from PIL import Image
import numpy as np

def image_blocks(image_path, block_size=64):

    # Standardize image
    img = Image.open(image_path)

    img = img.convert("L")        # grayscale
    img = img.resize((512, 512))  # fixed size

    arr = np.array(img)

    blocks = []

    for y in range(0, 512, block_size):
        for x in range(0, 512, block_size):

            block = arr[y:y+block_size, x:x+block_size]

            blocks.append(block.tobytes())

    return blocks