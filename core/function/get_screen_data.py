import cv2
import pytesseract
from main import CONFIG

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def get_frame_line_data(frame, value):
    x, y, w, h = CONFIG.get('values_map', value, 'tuple')
    frame = frame[y:y + h, x:x + w]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    TESS_CFG = (
        ' --oem 1'
        ' --psm 12'  # 6 best result for now, 12 also good
        ' -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789:'
        ' -c preserve_interword_spaces=1'
    )

    text = pytesseract.image_to_string(gray, lang='eng').replace('\n', '')
    data = pytesseract.image_to_data(gray, config=TESS_CFG, output_type=pytesseract.Output.DICT)

    return text if text in data['text'] else None