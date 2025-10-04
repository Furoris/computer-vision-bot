import cv2

# Try 0..5 to find the OBS Virtual Camera index
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # Try 0..5 to find the OBS Virtual Camera index
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():
    raise RuntimeError("Could not open OBS Virtual Camera. Try another index (0..5).")

def get_frame():
    returned, frame = cap.read()

    if not returned:
        raise RuntimeError("Could not open OBS Virtual Camera. Try another index (0..5).")

    return frame
