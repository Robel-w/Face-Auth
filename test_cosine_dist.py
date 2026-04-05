import cv2
import pickle
import numpy as np

with open("models/face_model.pkl", "rb") as f:
    model = pickle.load(f)

print("Classes:", model.classes_)

# Let's generate a totally random image (simulating a random person)
random_img = np.random.randint(0, 255, (64, 64), dtype=np.uint8)
hog = cv2.HOGDescriptor((64, 64), (16, 16), (8, 8), (8, 8), 9)
random_vec = hog.compute(random_img).flatten().reshape(1, -1)

# Real image
real_img = cv2.imread("data/raw/yabets maregn/0.jpg", cv2.IMREAD_GRAYSCALE)
real_img = cv2.resize(real_img, (64, 64))
real_vec = hog.compute(real_img).flatten().reshape(1, -1)

distances_rand, _ = model.kneighbors(random_vec)
distances_real, _ = model.kneighbors(real_vec)

print("Random Image Distance (Cosine):", np.mean(distances_rand))
print("Real Image Distance (Cosine):", np.mean(distances_real))
