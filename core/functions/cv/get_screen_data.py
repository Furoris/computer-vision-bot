import cv2
import pytesseract
from main import CONFIG
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def get_frame_line_data(frame, value):
    x, y, w, h = CONFIG.get('values_map', value, 'tuple')
    frame = frame[y:y + h, x:x + w]
    frame = add_top_image_separator(frame)
    frame = transform_frame(frame)

    TESS_CFG = (
        ' --oem 1'
        ' --psm 6'  # 6 best result for now, 12 also good
        ' -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789/:'
        ' -c preserve_interword_spaces=1'
    )

    # get value from two sources and compare them to increase validity of value
    text = pytesseract.image_to_string(frame, lang='eng', config=TESS_CFG).replace('\n', '')
    data = pytesseract.image_to_data(frame, config=TESS_CFG, output_type=pytesseract.Output.DICT)

    return text if text in data['text'] else None


def add_top_image_separator(frame):
    #adding grey bar to top of frame to better separate value to be recognized
    h, w, c = frame.shape
    grey_row = np.full((1, w, c), 128, dtype=np.uint8)

    return np.vstack((grey_row, frame))


def transform_frame(frame):
    #transform image to gray scale to increase recognition chance
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
    frame = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    frame = cv2.medianBlur(frame, 3)

    return frame