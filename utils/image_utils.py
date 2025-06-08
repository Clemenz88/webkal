
import cv2
from PIL import Image
import numpy as np

def load_image(img_file):
    return Image.open(img_file)

def detect_hand_and_food_area(image):
    return 1.0  # dummy scale

def compute_scale_cm2(scale_factor):
    return scale_factor
