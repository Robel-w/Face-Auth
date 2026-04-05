import sys; sys.path.append('.')
from src.feature_engineering import load_dataset
X, y, label_map = load_dataset()
print("Y array:", y)
print("Label Map:", label_map)
