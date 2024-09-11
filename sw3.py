import pygame
import pyautogui
import pygetwindow as gw
import win32gui
import win32con
import sys
import cv2
import numpy as np
import keyboard
import time
import mouse
import win32api
from mss import mss

# Initialize Pygame
pygame.init()

# Window settings
window_title = 'Squad Game Magnifier'
window_width, window_height = 2100, 2100
screen = pygame.display.set_mode((window_width, window_height), pygame.NOFRAME)
pygame.display.set_caption(window_title)

# Magnification factor
magnification_factor = 3

# Screen resolution
screen_width, screen_height = pyautogui.size()

# Initial window position
initial_x = (screen_width - window_width) // 2 + 1400
initial_y = (screen_height - window_height) // 2

# Set window always on top and move to initial position
window = gw.getWindowsWithTitle(window_title)[0]
win32gui.SetWindowPos(window._hWnd, win32con.HWND_TOPMOST, initial_x, initial_y, 0, 0, win32con.SWP_NOSIZE)

# Prevent window from gaining focus
ex_style = win32gui.GetWindowLong(window._hWnd, win32con.GWL_EXSTYLE)
win32gui.SetWindowLong(window._hWnd, win32con.GWL_EXSTYLE, ex_style | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_LAYERED)

# Set window transparency
win32gui.SetLayeredWindowAttributes(window._hWnd, win32api.RGB(0,0,0), 0, win32con.LWA_COLORKEY)

# Window visibility state
window_visible = False

# Show and hide window functions
def toggle_window():
    global window_visible
    if not window_visible:
        win32gui.ShowWindow(window._hWnd, win32con.SW_SHOW)
        window_visible = True
    else:
        win32gui.ShowWindow(window._hWnd, win32con.SW_HIDE)
        window_visible = False

# Hide window initially
win32gui.ShowWindow(window._hWnd, win32con.SW_HIDE)
keyboard.block_key('Win')

# Initialize mss
sct = mss()

# Initialize VideoCapture for screen capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

if_smap_key_pressed = False
# Main loop
running = True
frame_interval = 1 / 120  # 120Hz frame interval
use_mss = True  # Toggle between mss and cv2.VideoCapture

while running:
    if not if_smap_key_pressed and keyboard.is_pressed('x'):
        if_smap_key_pressed = True
        toggle_window()
    elif if_smap_key_pressed and (not keyboard.is_pressed('x')):
        if_smap_key_pressed = False

    if win32gui.IsWindowVisible(window._hWnd) and mouse.get_position()[0] > 2400:
        mouse.move(2400, mouse.get_position()[1], absolute=True, duration=0)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Screen capture region
    center_x, center_y = screen_width // 2, screen_height // 2
    capture_width = window_width // magnification_factor
    capture_height = window_height // magnification_factor
    left = center_x - (capture_width // 2)
    top = center_y - (capture_height // 2)
    
    if use_mss:
        # Capture and magnify screen using mss
        monitor = {"top": top, "left": left, "width": capture_width, "height": capture_height}
        screenshot = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(screenshot, cv2.COLOR_RGBA2RGB)
    else:
        # Capture and magnify screen using cv2.VideoCapture
        ret, full_frame = cap.read()
        if not ret:
            continue
        frame = full_frame[top:top+capture_height, left:left+capture_width]

    #frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    frame = cv2.flip(frame, 1)
    magnified_image = cv2.resize(frame, (window_width, window_height), interpolation=cv2.INTER_NEAREST)
    magnified_image = cv2.cvtColor(magnified_image, cv2.COLOR_BGR2RGB)
    pygame_image = pygame.surfarray.make_surface(magnified_image)

    screen.fill((0, 0, 0))  # Fill with black color
    screen.blit(pygame_image, (0, 0))
    
    pygame.display.update()

    #time.sleep(frame_interval)

pygame.quit()
cap.release()
sys.exit()