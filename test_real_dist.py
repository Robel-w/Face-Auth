import cv2
import pickle
import numpy as np
from src.preprocessing import detect_and_crop_face, preprocess_face
from src.feature_engineering import image_to_vector

with open("models/face_model.pkl", "rb") as f:
    model = pickle.load(f)

# Real image
img_path = "data/raw/yabets maregn/0.jpg"
image = cv2.imread(img_path)
cropped = detect_and_crop_face(image)
processed = preprocess_face(cropped)
real_vec = image_to_vector(processed).reshape(1, -1)

# Random image
random_img = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)
# bypass detection since face cascade will fail
rand_processed = preprocess_face(random_img)
rand_vec = image_to_vector(rand_processed).reshape(1, -1)

distances_rand, _ = model.kneighbors(rand_vec)
distances_real, _ = model.kneighbors(real_vec)

print("Random Image Distance (Cosine):", np.mean(distances_rand))
print("Real Image Distance (Cosine):", np.mean(distances_real))
