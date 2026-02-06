import cv2
import numpy as np
from PIL import Image, ImageEnhance
import os

def load_image(image_path: str):
    return cv2.imread(image_path)

def save_image(image, output_path: str):
    cv2.imwrite(output_path, image)

def denoise(image):
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

def increase_brightness(image, value=30):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    
    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value
    
    final_hsv = cv2.merge((h, s, v))
    image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return image

def increase_contrast(image, alpha=1.5, beta=0):
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

def sharpen(image):
    kernel = np.array([[0, -1, 0], 
                       [-1, 5,-1], 
                       [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)

def to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def blur(image):
    return cv2.GaussianBlur(image, (5, 5), 0)
    
def resize_image(image, width=None, height=None):
    if width is None and height is None:
        return image
        
    (h, w) = image.shape[:2]
    
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    elif height is None:
        r = width / float(w)
        dim = (width, int(h * r))
    else:
        dim = (width, height)
        
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

def enhance_auto(image):
    image = denoise(image)
    image = increase_contrast(image, 1.2, 10)
    image = increase_brightness(image, 10)
    image = sharpen(image)
    return image


    
def apply_filter(image_path: str, filter_type: str, output_path: str, params: dict = None):
    image = load_image(image_path)
    if image is None:
        raise ValueError("Could not load image")

    if filter_type == 'denoise':
        processed = denoise(image)
    elif filter_type == 'brightness':
        processed = increase_brightness(image)
    elif filter_type == 'contrast':
        processed = increase_contrast(image)
    elif filter_type == 'sharpen':
        processed = sharpen(image)
    elif filter_type == 'grayscale':
        processed = to_grayscale(image)
    elif filter_type == 'blur':
        processed = blur(image)
    elif filter_type == 'auto':
        processed = enhance_auto(image)
    elif filter_type == 'resize':
        w = params.get('width') if params else None
        h = params.get('height') if params else None
        processed = resize_image(image, width=w, height=h)
    else:
        processed = image # No change
        
    save_image(processed, output_path)
    return output_path
