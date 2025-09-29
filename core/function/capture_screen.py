import cv2
import pytesseract

# Try 0..5 to find the OBS Virtual Camera index
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # Try 0..5 to find the OBS Virtual Camera index
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():
    raise RuntimeError("Could not open OBS Virtual Camera. Try another index (0..5).")

# region of your minimap in the OBS canvas (x,y,w,h)
MINIMAP_ROI = (0, 0, 1920, 1080)
SKILLS = (1506,25,184,234)# adjust to your OBS canvas coordinates
MANA_VALUE = (1656, 124, 31, 16)

def get_frame():
    returned, frame = cap.read()

    if not returned:
        raise RuntimeError("Could not open OBS Virtual Camera. Try another index (0..5).")

    return frame
