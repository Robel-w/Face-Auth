import re
with open("app/api.py", "r") as f:
    text = f.read()

# Replace massive loops with 20 fast samples
text = re.sub(r'for i in range\(1, 100\):', 'for i in range(1, 10):', text)
text = re.sub(r'for i in range\(101, 200\):', 'for i in range(11, 20):', text)

# Replace subprocess with direct function call
old_subprocess = '''def _train_model_background():
    env = os.environ.copy()
    env["PYTHONPATH"] = BASE_DIR
    import logging
    try:
        res = subprocess.run([sys.executable, TRAIN_SCRIPT], env=env, cwd=BASE_DIR, capture_output=True, text=True)
        if res.returncode != 0:
             print("Background training failed:\\nSTDOUT:\\n", res.stdout, "\\nSTDERR:\\n", res.stderr)
        else:
             print("Background training succeeded.")
    except Exception as e:
        print(f"Subprocess failed: {e}")'''

new_direct_call = '''def _train_model_background():
    try:
        from src.feature_engineering import load_dataset
        from src.train import train_model
        from config import MODELS_DIR, MODEL_NAME
        import os, pickle
        
        os.makedirs(MODELS_DIR, exist_ok=True)
        X, y, label_map = load_dataset()
        
        label_map_path = os.path.join(MODELS_DIR, "label_map.pkl")
        with open(label_map_path, "wb") as f:
            pickle.dump(label_map, f)
            
        model_path = os.path.join(MODELS_DIR, MODEL_NAME)
        train_model(X, y, model_path)
        print("Background training completed successfully in-process.")
    except Exception as e:
        print(f"Background training failed: {e}")'''

if old_subprocess in text:
    text = text.replace(old_subprocess, new_direct_call)
    print("Patched background task.")
else:
    print("Could not find subprocess logic.")

with open("app/api.py", "w") as f:
    f.write(text)
