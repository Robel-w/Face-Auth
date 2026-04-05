import cv2
import numpy as np
import os
from src.preprocessing import detect_and_crop_face, preprocess_face

hog_descriptor = cv2.HOGDescriptor(
    _winSize=(64,64),
    _blockSize=(16,16),
    _blockStride=(8,8),
    _cellSize=(8,8),
    _nbins=9)

def get_hog_vec(user):
    img_path = os.path.join('data/raw', user, os.listdir(os.path.join('data/raw', user))[0])
    img = cv2.imread(img_path)
    processed = preprocess_face(detect_and_crop_face(img))
    processed_uint8 = (processed * 255.0).astype(np.uint8)
    hog_features = hog_descriptor.compute(processed_uint8)
    return hog_features.flatten()

users = os.listdir('data/raw')
vecs = {u: get_hog_vec(u) for u in users}

for u1 in users:
    for u2 in users:
        dist = np.linalg.norm(vecs[u1] - vecs[u2])
        print(f"Dist {u1} -> {u2} = {dist}")
