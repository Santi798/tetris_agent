import ctypes
from ctypes import wintypes


user32 = ctypes.WinDLL('user32', use_last_error=True)

# Constantes.
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008

# Estructuras necesarias para alineación y llamada al SO.
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)),
    ]

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)),
    ]

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    ]

class INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("ki", KEYBDINPUT),
        ("mi", MOUSEINPUT),
        ("hi", HARDWAREINPUT),
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("u", INPUT_UNION), # La unión va aquí.
    ]

def send_input(vk, flags):
    # Inicializamos la estructura con la unión.
    extra = ctypes.pointer(wintypes.ULONG(0))
    ii_ = INPUT_UNION()
    ii_.ki = KEYBDINPUT(vk, 0, flags, 0, extra)
    
    x = INPUT(type=INPUT_KEYBOARD, u=ii_)
    
    # Tamaño correcto de la estructura.
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

class KeysController:

    @staticmethod
    def press_key(vk):
        send_input(vk, 0)

    @staticmethod
    def release_key(vk):
        send_input(vk, KEYEVENTF_KEYUP)

    def tap(self, vk):
        self.press_key(vk)
        self.release_key(vk)
