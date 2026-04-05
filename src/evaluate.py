import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    return {
        "accuracy": acc,
        "confusion_matrix": cm
    }

if __name__ == "__main__":
    print("Evaluate can be integrated dynamically after training or on a separate testing set.")

