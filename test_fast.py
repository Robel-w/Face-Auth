import pickle
import numpy as np

with open("models/face_model.pkl", "rb") as f:
    model = pickle.load(f)

X_train = model._fit_X
y_train = model._y

c0 = X_train[y_train == 0]
c1 = X_train[y_train == 1]

# Distances from c0 to ALL of c0
dists_0_to_0 = []
for i in range(10):
    dist, _ = model.kneighbors(c0[i:i+1], n_neighbors=2)
    dists_0_to_0.append(dist[0][1])  # avoid self (0)
print("Min dist self c0:", np.mean(dists_0_to_0))

dists_1_to_0 = []
for i in range(10):
    dist_mat = np.linalg.norm(c0 - c1[i], axis=1)
    dists_1_to_0.append(np.min(dist_mat))
print("Min dist c1 to c0:", np.mean(dists_1_to_0))
