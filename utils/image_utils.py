import cv2
import numpy as np
from PIL import Image

def load_image(uploaded_file):
    image = Image.open(uploaded_file)
    return np.array(image)

def detect_hand_and_food_area(image):
    hand_area = 100.0
    food_area = 250.0
    return hand_area, food_area