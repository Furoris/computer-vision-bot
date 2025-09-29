import ctypes
from ctypes import wintypes
import time
import random

user32 = ctypes.WinDLL("user32", use_last_error=True)

# --- constants ---
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1

# KEYEVENTF flags
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
KEYEVENTF_SCANCODE    = 0x0008

# MOUSEEVENTF flags
MOUSEEVENTF_MOVE        = 0x0001
MOUSEEVENTF_LEFTDOWN    = 0x0002
MOUSEEVENTF_LEFTUP      = 0x0004
MOUSEEVENTF_RIGHTDOWN   = 0x0008
MOUSEEVENTF_RIGHTUP     = 0x0010
MOUSEEVENTF_MIDDLEDOWN  = 0x0020
MOUSEEVENTF_MIDDLEUP    = 0x0040
MOUSEEVENTF_WHEEL       = 0x0800
MOUSEEVENTF_HWHEEL      = 0x01000
MOUSEEVENTF_ABSOLUTE    = 0x8000

MAPVK_VK_TO_VSC = 0

# Some VKs you’ll likely need
VK = {
    "lbutton": 0x01, "rbutton": 0x02, "mbutton": 0x04,
    "back": 0x08, "tab": 0x09, "enter": 0x0D, "shift": 0x10,
    "ctrl": 0x11, "alt": 0x12, "pause": 0x13, "esc": 0x1B, "space": 0x20,
    "left": 0x25, "up": 0x26, "right": 0x27, "down": 0x28,
    "insert": 0x2D, "delete": 0x2E, "home": 0x24, "end": 0x23, "pgup": 0x21, "pgdn": 0x22,
    "0":0x30,"1":0x31,"2":0x32,"3":0x33,"4":0x34,"5":0x35,"6":0x36,"7":0x37,"8":0x38,"9":0x39,
    "a":0x41,"b":0x42,"c":0x43,"d":0x44,"e":0x45,"f":0x46,"g":0x47,"h":0x48,"i":0x49,"j":0x4A,
    "k":0x4B,"l":0x4C,"m":0x4D,"n":0x4E,"o":0x4F,"p":0x50,"q":0x51,"r":0x52,"s":0x53,"t":0x54,
    "u":0x55,"v":0x56,"w":0x57,"x":0x58,"y":0x59,"z":0x5A,
    "f1":0x70,"f2":0x71,"f3":0x72,"f4":0x73,"f5":0x74,"f6":0x75,"f7":0x76,"f8":0x77,
    "f9":0x78,"f10":0x79,"f11":0x7A,"f12":0x7B,
    "numlock":0x90, "scroll":0x91, "rshift":0xA1, "lmenu":0xA4, "rmenu":0xA5, "lcontrol":0xA2, "rcontrol":0xA3
}

# Extended keys per MS docs (arrows, ins/del/home/end/pgup/pgdn, numpad divide, RCTRL/RALT, etc.)
EXTENDED_VKS = {
    VK["left"], VK["right"], VK["up"], VK["down"],
    VK["insert"], VK["delete"], VK["home"], VK["end"], VK["pgup"], VK["pgdn"],
    VK["rcontrol"], VK["rmenu"], VK["numlock"]
}

# --- structures ---
ULONG_PTR = wintypes.WPARAM

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", ULONG_PTR))

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",        wintypes.DWORD),
                ("wParamL",     wintypes.WORD),
                ("wParamH",     wintypes.WORD))

class INPUT_UNION(ctypes.Union):
    _fields_ = (("mi", MOUSEINPUT),
                ("ki", KEYBDINPUT),
                ("hi", HARDWAREINPUT))

class INPUT(ctypes.Structure):
    _anonymous_ = ("u",)
    _fields_ = (("type", wintypes.DWORD),
                ("u", INPUT_UNION))

# Prototype
user32.SendInput.restype  = wintypes.UINT
user32.SendInput.argtypes = (wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int)
user32.MapVirtualKeyW.restype  = wintypes.UINT
user32.MapVirtualKeyW.argtypes = (wintypes.UINT, wintypes.UINT)

def _raise_if_failed(sent, expected):
    if sent != expected:
        err = ctypes.get_last_error()
        raise ctypes.WinError(err or 5)  # 5 = ACCESS_DENIED often means not elevated vs elevated target

# --- keyboard helpers ---
def _scan_from_vk(vk):
    return user32.MapVirtualKeyW(vk, MAPVK_VK_TO_VSC)

def key_event_vk(vk, down=True, use_scancode=True):
    flags = 0
    wVk, wScan = 0, 0
    if use_scancode:
        wScan = _scan_from_vk(vk)
        flags |= KEYEVENTF_SCANCODE
        if vk in EXTENDED_VKS:
            flags |= KEYEVENTF_EXTENDEDKEY
    else:
        wVk = vk
    if not down:
        flags |= KEYEVENTF_KEYUP
    inp = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(wVk, wScan, flags, 0, 0))
    return inp

def press_vk(vk, hold=0.02):
    arr = (INPUT * 2)(
        key_event_vk(vk, True),
        key_event_vk(vk, False)
    )
    sent = user32.SendInput(2, arr, ctypes.sizeof(INPUT))
    _raise_if_failed(sent, 2)
    time.sleep(hold)

def press(name, hold=0.02):
    print('press', name)
    vk = VK.get(name.lower())
    if vk is None:
        raise ValueError(f"Unknown key name: {name}")
    press_vk(vk, hold)

def press_combo(names, key_hold=0.02, between=0.01):
    vks = [VK[n.lower()] for n in names]
    downs = [INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(0, _scan_from_vk(vk),
               KEYEVENTF_SCANCODE | (KEYEVENTF_EXTENDEDKEY if vk in EXTENDED_VKS else 0), 0, 0))
             for vk in vks]
    ups = [INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(0, _scan_from_vk(vk),
             KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | (KEYEVENTF_EXTENDEDKEY if vk in EXTENDED_VKS else 0), 0, 0))
           for vk in reversed(vks)]
    # down all
    sent = user32.SendInput(len(downs), (INPUT * len(downs))(*downs), ctypes.sizeof(INPUT))
    _raise_if_failed(sent, len(downs))
    time.sleep(key_hold)
    # up all (reverse order)
    sent = user32.SendInput(len(ups), (INPUT * len(ups))(*ups), ctypes.sizeof(INPUT))
    _raise_if_failed(sent, len(ups))
    time.sleep(between)

def type_text(text, per_char_delay=(0.0, 0.0)):
    # Unicode path: set KEYEVENTF_UNICODE and put the wchar code point in wScan, wVk must be 0.
    inps = []
    for ch in text:
        cp = ord(ch)
        kd = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(0, cp, KEYEVENTF_UNICODE, 0, 0))
        ku = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(0, cp, KEYEVENTF_UNICODE | KEYEVENTF_KEYUP, 0, 0))
        inps.extend([kd, ku])
    # send in batches to avoid gigantic arrays
    for i in range(0, len(inps), 64):
        batch = inps[i:i+64]
        sent = user32.SendInput(len(batch), (INPUT * len(batch))(*batch), ctypes.sizeof(INPUT))
        _raise_if_failed(sent, len(batch))
        if per_char_delay != (0.0, 0.0):
            time.sleep(random.uniform(*per_char_delay))

# --- mouse helpers ---
def move_mouse_abs(x, y, screen_w=None, screen_h=None):
    # Normalize to 0..65535 absolute coords
    if screen_w is None: screen_w = user32.GetSystemMetrics(0)
    if screen_h is None: screen_h = user32.GetSystemMetrics(1)
    nx = int(x * 65535 // (screen_w - 1))
    ny = int(y * 65535 // (screen_h - 1))
    inp = INPUT(type=INPUT_MOUSE, mi=MOUSEINPUT(nx, ny, 0, MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, 0, 0))
    sent = user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))
    _raise_if_failed(sent, 1)

def click_left_abs(x, y, hold=0.02):
    move_mouse_abs(x, y)
    down = INPUT(type=INPUT_MOUSE, mi=MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTDOWN, 0, 0))
    up   = INPUT(type=INPUT_MOUSE, mi=MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTUP,   0, 0))
    sent = user32.SendInput(1, ctypes.byref(down), ctypes.sizeof(INPUT))
    _raise_if_failed(sent, 1)
    time.sleep(hold)
    sent = user32.SendInput(1, ctypes.byref(up), ctypes.sizeof(INPUT))
    _raise_if_failed(sent, 1)
