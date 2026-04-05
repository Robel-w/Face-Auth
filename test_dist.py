import cv2
import numpy as np
import pickle
import os
from src.preprocessing import detect_and_crop_face, preprocess_face
from src.feature_engineering import image_to_vector

model = pickle.load(open('models/face_model.pkl','rb'))
with open('models/label_map.pkl', 'rb') as f:
    label_map = pickle.load(f)

for user in os.listdir('data/raw'):
    print("Testing user", user)
    img_path = os.path.join('data/raw', user, os.listdir(os.path.join('data/raw', user))[0])
    img = cv2.imread(img_path)
    cropped = detect_and_crop_face(img)
    processed = preprocess_face(cropped)
    features = image_to_vector(processed).reshape(1, -1)
    dists, _ = model.kneighbors(features)
    print(f"Dist to closest for {user}: {np.mean(dists[0])}")

