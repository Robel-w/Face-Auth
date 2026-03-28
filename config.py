from pathlib import Path

# Base project paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
MODELS_DIR = BASE_DIR / "models"

# Capture / training parameters
CAPTURE_SAMPLES = 20
IMAGE_SIZE = (160, 160)
MODEL_NAME = "face_model.pkl"

def ensure_dirs():
    for p in (RAW_DIR, PROCESSED_DIR, MODELS_DIR):
        p.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    ensure_dirs()
