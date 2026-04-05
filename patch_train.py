import re
with open("src/train.py", "r") as f:
    text = f.read()

# Add os.makedirs
new_logic = '''if __name__ == "__main__":
    try:
        os.makedirs(MODELS_DIR, exist_ok=True)
        X, y, label_map = load_dataset()'''

text = text.replace('''if __name__ == "__main__":
    try:
        X, y, label_map = load_dataset()''', new_logic)

with open("src/train.py", "w") as f:
    f.write(text)
