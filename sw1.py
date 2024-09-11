import pygame
from PIL import ImageGrab, Image
import pyautogui  # 用于获取屏幕分辨率
import pygetwindow as gw
import win32gui
import win32con
import sys
import mouse

# 初始化Pygame
pygame.init()

# 设置窗口标题大小和位置 (放大显示窗口)
window_title='Squad Game Magnifier'
window_width = 1000  # 最终显示的窗口宽度
window_height = 500  # 最终显示的窗口高度

# 设置窗口为无边框模式
screen = pygame.display.set_mode((window_width, window_height), pygame.NOFRAME)
pygame.display.set_caption(window_title)

# 放大倍数
magnification_factor = 2  # 放大倍数

# 使用pyautogui获取屏幕分辨率
screen_width, screen_height = pyautogui.size()

# 计算窗口的初始位置，使其垂直居中并贴在屏幕顶部
initial_x = (screen_width - window_width) // 2
initial_y = 0

# 设置窗口总在最顶层并移动到初始位置
window = gw.getWindowsWithTitle(window_title)[0]  # 获取窗口对象
win32gui.SetWindowPos(window._hWnd, win32con.HWND_TOPMOST, initial_x, initial_y, 0, 0, win32con.SWP_NOSIZE)

# 阻止窗口获取焦点
ex_style = win32gui.GetWindowLong(window._hWnd, win32con.GWL_EXSTYLE)
win32gui.SetWindowLong(window._hWnd, win32con.GWL_EXSTYLE, ex_style | win32con.WS_EX_NOACTIVATE)

# 计算截取区域（按放大倍数反向计算出截图区域大小）
grab_width = window_width // magnification_factor  # 实际需要截取的宽度
grab_height = window_height // magnification_factor  # 实际需要截取的高度

# 主循环
running = True
while running:

    if win32gui.IsWindowVisible(window._hWnd) and mouse.get_position()[1] < 600:
        mouse.move(mouse.get_position()[0], 600, absolute=True, duration=0)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 获取屏幕中心坐标
    center_x, center_y = screen_width // 2, screen_height // 2

    # 计算屏幕中心的截取区域（放大后的图像恰好填满窗口）
    bbox = (center_x - grab_width // 2, center_y - grab_height // 2,
            center_x + grab_width // 2, center_y + grab_height // 2)
    screenshot = ImageGrab.grab(bbox)

    # 放大截图（使用较快的最近邻插值算法）
    magnified_image = screenshot.resize((window_width, window_height), Image.NEAREST)

    # 将Pillow图像转换为Pygame图像
    mode = magnified_image.mode
    size = magnified_image.size
    data = magnified_image.tobytes()

    pygame_image = pygame.image.fromstring(data, size, mode)

    # 清除屏幕
    screen.fill((0, 0, 0))

    # 将放大的图像绘制到Pygame窗口
    screen.blit(pygame_image, (0, 0))

    # 更新显示
    pygame.display.update()

# 退出Pygame
pygame.quit()
sys.exit()