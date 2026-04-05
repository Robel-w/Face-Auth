import cv2
import numpy as np
import pickle
import os
from src.preprocessing import detect_and_crop_face, preprocess_face
from src.feature_engineering import image_to_vector

def get_vec(img_path):
    img = cv2.imread(img_path)
    cropped = detect_and_crop_face(img)
    if cropped is None: return None
    processed = preprocess_face(cropped)
    if processed is None: return None
    return image_to_vector(processed).reshape(1, -1)

users = os.listdir('data/raw')
for u in users:
    imgs = os.listdir(os.path.join('data/raw', u))[:10]
    vecs = []
    for i in imgs:
        v = get_vec(os.path.join('data/raw', u, i))
        if v is not None: vecs.append(v)
    for i in range(1, len(vecs)):
        print(f"{u} image 0 to {i}: {np.linalg.norm(vecs[0] - vecs[i])}")
