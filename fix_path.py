import re
with open("src/feature_engineering.py", "r") as f:
    text = f.read()

text = text.replace('DATASET_PATH = "data/raw/"', 'import os; BASE_DIR = os.path.dirname(os.path.dirname(__file__)); DATASET_PATH = os.path.join(BASE_DIR, "data", "raw")')

with open("src/feature_engineering.py", "w") as f:
    f.write(text)
