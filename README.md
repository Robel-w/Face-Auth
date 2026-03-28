# Face-Auth

Project scaffold for a simple face-authentication demo using Streamlit.

Project structure

```
│
├── app/                        # Streamlit application (UI layer)
│   ├── main.py                # Entry point (run this file)
│   ├── pages/
│   │   ├── register.py
│   │   └── login.py
│   └── utils.py               # Helper functions for UI
│
├── data/                      # Dataset (NOT pushed to GitHub ideally)
│   ├── raw/                   # Original captured images
│   └── processed/             # Preprocessed images (optional)
│
├── models/                    # Saved ML models
│   └── face_model.pkl
│
├── src/                       # Core ML logic (VERY IMPORTANT)
│   ├── data_collection.py     # Webcam capture logic
│   ├── preprocessing.py       # Face detection, resizing, cleaning
│   ├── feature_engineering.py # Flattening, transformations
│   ├── train.py               # Model training script
│   ├── evaluate.py            # Evaluation metrics
│   └── predict.py             # Inference logic
│
├── notebooks/                 # Optional experimentation (Jupyter)
│   └── exploration.ipynb
│
├── tests/
│   └── test_pipeline.py
│
├── requirements.txt           # Dependencies
├── README.md                  # Project documentation
├── .gitignore                 # Ignore unnecessary files
└── config.py                  # Configurations (paths, parameters)
```
