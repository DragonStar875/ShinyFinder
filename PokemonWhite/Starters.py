import pyautogui
import keyboard
import time
from pyautogui import ImageNotFoundException

# --- Constants ---
WAIT_TIME = 0.5
KEY_DELAY = 0.1
CONFIDENCE = 0.8

TARGET_IMAGE = r"C:\Users\Nash\PycharmProjects\ShinyFinder\PokemonWhite\pokeball.png"
RESET_FILE = r"C:\Users\Nash\PycharmProjects\ShinyFinder\PokemonWhite\resets.txt"
SHINY_IMAGE = r"C:\Users\Nash\Pictures\Shinies\ShinySnivy.png"
PIXEL_CHECK_COORDS = (992, 824)
PIXEL_TARGET_RED = 24

# --- Utilities ---
def press_key(key: str, hold: float = KEY_DELAY):
    pyautogui.keyDown(key)
    time.sleep(hold)
    pyautogui.keyUp(key)

def soft_reset():
    for key in ['q', 'e', 't', 'y']:
        pyautogui.keyDown(key)
    time.sleep(KEY_DELAY)
    for key in ['q', 'e', 't', 'y']:
        pyautogui.keyUp(key)

def find_image(image_path: str, confidence: float = CONFIDENCE) -> bool:
    try:
        return pyautogui.locateCenterOnScreen(image_path, confidence=confidence) is not None
    except ImageNotFoundException:
        return False

def main_loop() -> int:
    soft_reset()
    time.sleep(WAIT_TIME)

    while not find_image(TARGET_IMAGE):
        press_key('f')
        time.sleep(WAIT_TIME)

    for _ in range(5):
        press_key('a')
        time.sleep(WAIT_TIME)

    counter = 0
    while pyautogui.pixel(*PIXEL_CHECK_COORDS)[0] != PIXEL_TARGET_RED:
        press_key('f')
        time.sleep(WAIT_TIME)

    while pyautogui.pixel(*PIXEL_CHECK_COORDS)[0] == PIXEL_TARGET_RED:
        counter += 1

    return counter

def read_resets() -> int:
    try:
        with open(RESET_FILE, "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

def write_resets(resets: int):
    with open(RESET_FILE, "w") as f:
        f.write(str(resets))

def count_down(seconds: int):
    for i in range(seconds, 0, -1):
        print(i)
        time.sleep(WAIT_TIME)
    print("Program Starting")

# --- Main Execution ---
if __name__ == "__main__":
    count_down(5)

    print("Calibrating...")
    shiny_threshold = main_loop() + 10
    print("Setting threshold to:", shiny_threshold)

    resets = read_resets()
    print("Program begin")

    try:
        while True:
            if keyboard.is_pressed('space'):
                print("Spacebar pressed. Saving and exiting...")
                write_resets(resets)
                break

            if main_loop() >= shiny_threshold:
                pyautogui.screenshot().save(SHINY_IMAGE)
                print("SHINY!!!")
                print("Total resets:", resets)
                break

            resets += 1
            print("Resets:", resets)

    except KeyboardInterrupt:
        print("Interrupted manually.")
        write_resets(resets)
