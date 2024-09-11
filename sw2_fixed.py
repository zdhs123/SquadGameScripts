import pygame
from PIL import Image
import pyautogui
import pygetwindow as gw
import win32gui
import win32con
import sys
import bettercam
import keyboard
import time
import mouse
import win32api
import matplotlib.pyplot as plt
#import numpy as np

## 绘制空心圆
#def draw_hollow_circle():
#    radius = 100
#    center_x, center_y = 0, 0
#
#    theta = np.linspace(0, 2 * np.pi, 100)
#    x = center_x + radius * np.cos(theta)
#    y = center_y + radius * np.sin(theta)
#
#    plt.figure()
#    plt.plot(x, y, 'b')  # 'b' 表示蓝色
#    plt.gca().set_aspect('equal', adjustable='box')
#    plt.title('空心圆')
#    plt.show()
#
## 调用绘制空心圆函数
#draw_hollow_circle()

# Initialize Pygame
pygame.init()

# Window settings
window_title = 'Squad Game Magnifier'
window_width, window_height = 2400, 1000
screen = pygame.display.set_mode((window_width, window_height), pygame.NOFRAME)
pygame.display.set_caption(window_title)

# Magnification factor
magnification_factor = 4

# Screen resolution
screen_width, screen_height = pyautogui.size()

# Initial window position
#initial_x = (screen_width - window_width) // 2 + 1400
initial_x = (screen_width - window_width) // 2
#initial_y = (screen_height - window_height) // 2
initial_y = screen_height - window_height
#initial_y = 0

# Set window always on top and move to initial position
window = gw.getWindowsWithTitle(window_title)[0]
win32gui.SetWindowPos(window._hWnd, win32con.HWND_TOPMOST, initial_x, initial_y, 0, 0, win32con.SWP_NOSIZE)

# Prevent window from gaining focus
ex_style = win32gui.GetWindowLong(window._hWnd, win32con.GWL_EXSTYLE)
win32gui.SetWindowLong(window._hWnd, win32con.GWL_EXSTYLE, ex_style | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_LAYERED)

# Set window transparency
win32gui.SetLayeredWindowAttributes(window._hWnd, win32api.RGB(0,0,0), 0, win32con.LWA_COLORKEY)

# Create circular region
#hrgn = win32gui.CreateRoundRectRgn(0, 0, window_width, window_height, window_width, window_height)
#win32gui.SetWindowRgn(window._hWnd, hrgn, True)

# Initialize BetterCam
camera = bettercam.create(output_idx=0, output_color="RGB")

# Window visibility state
window_visible = False

# Show and hide window functions
def toggle_window():
    global window_visible
    if not window_visible:
        win32gui.ShowWindow(window._hWnd, win32con.SW_SHOW)
        window_visible=True
    else:
        win32gui.ShowWindow(window._hWnd, win32con.SW_HIDE)
        window_visible=False

# Hide window initially
#win32gui.ShowWindow(window._hWnd, win32con.SW_HIDE)
keyboard.block_key('Win')

# Bind hotkey
#keyboard.on_press_key('x', lambda _: toggle_window())

if_smap_key_pressed=False
# Main loop
running = True
frame_interval = 1 / 100  # 30Hz frame interval
while running:
    
    if not if_smap_key_pressed and keyboard.is_pressed('x'):
        if_smap_key_pressed=True
        toggle_window()
    elif if_smap_key_pressed and (not keyboard.is_pressed('x')):
        if_smap_key_pressed=False
        toggle_window()

    if win32gui.IsWindowVisible(window._hWnd) and mouse.get_position()[1] > 1500:
        mouse.move(mouse.get_position()[0], 1500, absolute=True, duration=0)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Screen capture region
    center_x, center_y = screen_width // 2, screen_height // 2
    left = center_x - (window_width // (2 * magnification_factor))
    top = center_y - (window_height // (2 * magnification_factor))
    right = center_x + (window_width // (2 * magnification_factor))
    bottom = center_y + (window_height // (2 * magnification_factor))
    region = (left, top, right, bottom)

    # Capture and magnify screen
    frame = camera.grab(region=region)
    if frame is not None:
        screenshot = Image.fromarray(frame)
        magnified_image = screenshot.resize((window_width, window_height), Image.NEAREST)
        pygame_image = pygame.image.fromstring(magnified_image.tobytes(), magnified_image.size, magnified_image.mode)

        screen.fill((0, 0, 0))  # Fill with black color
        screen.blit(pygame_image, (0, 0))
        
        #pygame.draw.circle(screen, (255, 0, 0), (window_width // 2, window_height // 2), 50)
        
        pygame.display.update()

    time.sleep(frame_interval)

pygame.quit()
sys.exit()