import cv2
import numpy as np
import pickle
import os
from src.preprocessing import detect_and_crop_face, preprocess_face
from src.feature_engineering import image_to_vector

model = pickle.load(open('models/face_model.pkl','rb'))

def get_vec(user):
    img_path = os.path.join('data/raw', user, os.listdir(os.path.join('data/raw', user))[0])
    img = cv2.imread(img_path)
    return image_to_vector(preprocess_face(detect_and_crop_face(img))).reshape(1, -1)

users = os.listdir('data/raw')
vecs = {u: get_vec(u) for u in users}

for u1 in users:
    for u2 in users:
        dist = np.linalg.norm(vecs[u1] - vecs[u2])
        print(f"Dist {u1} -> {u2} = {dist}")
