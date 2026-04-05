import re
with open("app/api.py", "r") as f:
    text = f.read()

old_str = '''def _train_model_background():
    env = os.environ.copy()
    env["PYTHONPATH"] = BASE_DIR
    subprocess.run([sys.executable, TRAIN_SCRIPT], env=env)'''

new_str = '''def _train_model_background():
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

if old_str in text:
    text = text.replace(old_str, new_str)
    with open("app/api.py", "w") as f:
        f.write(text)
    print("Fixed cwd in app/api.py")
else:
    print("Could not find old_str in app/api.py")
