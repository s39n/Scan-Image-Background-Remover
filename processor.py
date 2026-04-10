import numpy as np
from PIL import Image

def process_image_data(image, white_threshold=225, black_threshold=150):
    """
    Make white areas transparent and enhance black contrast.
    Expects a PIL Image, returns a PIL Image.
    """
    img = image.convert("RGBA")
    data = np.array(img)
    r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]

    # 1. Transparency: Identify near-white areas and make them transparent
    # Pixels where R, G, B are all > white_threshold
    white_areas = (r > white_threshold) & (g > white_threshold) & (b > white_threshold)
    data[white_areas] = [255, 255, 255, 0]

    # 2. Contrast: Identify dark areas (that aren't already transparent) and make them pure black
    # This makes the "black stand out" as requested.
    not_transparent = data[:, :, 3] > 0
    black_areas = (r < black_threshold) & (g < black_threshold) & (b < black_threshold) & not_transparent
    data[black_areas] = [0, 0, 0, 255]

    return Image.fromarray(data)
