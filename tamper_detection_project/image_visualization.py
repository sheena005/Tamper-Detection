import numpy as np
from PIL import Image, ImageDraw

def highlight_tampered_blocks(image_path, modified_blocks, block_size=64):

    img = Image.open(image_path).convert("RGB")
    img = img.resize((512,512))

    draw = ImageDraw.Draw(img)

    blocks_per_row = 512 // block_size

    for idx in modified_blocks:

        row = idx // blocks_per_row
        col = idx % blocks_per_row

        x1 = col * block_size
        y1 = row * block_size
        x2 = x1 + block_size
        y2 = y1 + block_size

        draw.rectangle([x1,y1,x2,y2], outline="red", width=4)

    return img