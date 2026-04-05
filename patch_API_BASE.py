import re
with open("app/main.py", "r") as f:
    text = f.read()

text = re.sub(r'API_BASE = "http://localhost:8001/api"', 
r'import os\nAPI_BASE = os.getenv("API_BASE_URL", "http://localhost:8001/api")', text)

with open("app/main.py", "w") as f:
    f.write(text)
