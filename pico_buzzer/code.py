"""
Early-Press Quiz Buzzer - RP2040 Pico W HID Keyboard
Arcade buttons on GP3-GP12 send keys '1'-'0'
NOTE: GP0,GP1 (UART0), GP2 (WiFi) are RESERVED on Pico W, so we skip them
"""
import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Skip GP0 (UART TX), GP1 (UART RX), GP2 (WiFi)
# GP3='1', GP4='2', GP5='3', ... GP12='0'
BUTTON_PINS = [
    board.GP3,   # Player 1 -> key '1'
    board.GP4,   # Player 2 -> key '2'
    board.GP5,   # Player 3 -> key '3'
    board.GP6,   # Player 4 -> key '4'
    board.GP7,   # Player 5 -> key '5'
    board.GP8,   # Player 6 -> key '6'
    board.GP9,   # Player 7 -> key '7'
    board.GP10,  # Player 8 -> key '8'
    board.GP11,  # Player 9 -> key '9'
    board.GP12,  # Player 10 -> key '0'
]

# Keycodes for '1' through '0' (1-9, then 0)
KEY_MAP = [
    Keycode.ONE, Keycode.TWO, Keycode.THREE, Keycode.FOUR, Keycode.FIVE,
    Keycode.SIX, Keycode.SEVEN, Keycode.EIGHT, Keycode.NINE, Keycode.ZERO,
]

# GPIO pin numbers for debug print (board.GPx doesn't expose pin number)
GPIO_NUMS = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

DEBOUNCE_MS = 50  # debounce time in milliseconds

# Setup buttons with internal pull-up
buttons = []
for pin in BUTTON_PINS:
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP  # internal pull-up, button connects to GND
    buttons.append(btn)

# Setup HID keyboard
keyboard = Keyboard(usb_hid.devices)

# State tracking
last_press_time = [0] * len(buttons)
was_pressed = [False] * len(buttons)

print("Quiz Buzzer Ready! GP3-GP12 -> Keys 1-9,0 (GP0,1,2 SKIPPED)")

while True:
    now = time.monotonic() * 1000  # current time in ms

    for i, btn in enumerate(buttons):
        pressed = not btn.value  # LOW = pressed (pull-up, button to GND)

        if pressed and not was_pressed[i]:
            # Button just pressed - check debounce
            if (now - last_press_time[i]) > DEBOUNCE_MS:
                keyboard.press(KEY_MAP[i])
                keyboard.release(KEY_MAP[i])
                last_press_time[i] = now
                key_char = str((i + 1) % 10)  # 1-9, then 0
                print(f"GP{GPIO_NUMS[i]} pressed -> key '{key_char}'")

        was_pressed[i] = pressed

    time.sleep(0.005)  # 5ms polling interval
