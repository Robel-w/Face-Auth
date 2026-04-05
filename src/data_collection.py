import cv2
import os
import sys
import argparse

HAAR_CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)

def capture_from_webcam(output_dir, num_samples=50):
    os.makedirs(output_dir, exist_ok=True)
    
    # Try different camera indices
    cap = None
    for i in range(4):
        cap = cv2.VideoCapture(i)
        if cap is not None and cap.isOpened():
            print(f"Successfully opened camera at index {i}")
            break
    
    if cap is None or not cap.isOpened():
        print("Error: Could not open any webcam device.", file=sys.stderr)
        return False
    
    count = 0
    print(f"Starting capture for {num_samples} frames...")
    
    while count < num_samples:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame from camera.", file=sys.stderr)
            break
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
        
        display_frame = frame.copy()
        
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cv2.rectangle(display_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
            file_path = os.path.join(output_dir, f"{count}.jpg")
            cv2.imwrite(file_path, frame)
            count += 1
            print(f"Captured {count}/{num_samples}")
            
            cv2.imshow("Registering Face...", display_frame)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
        else:
            cv2.putText(display_frame, "No face detected! Look at camera.", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            cv2.imshow("Registering Face...", display_frame)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    
    if count == 0:
        return False
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, required=True, help="User Name")
    args = parser.parse_args()
    
    output_dir = os.path.join("data", "raw", args.name)
    success = capture_from_webcam(output_dir, num_samples=50)
    
    if success:
        print(f"Successfully captured images for {args.name}")
        sys.exit(0)
    else:
        print("Capture failed.", file=sys.stderr)
        sys.exit(1)
