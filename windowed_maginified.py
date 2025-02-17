'''
我需要一个python代码，需求如下：
1、使用win32库建立窗口界面，窗口的大小为宽度300的正方形，窗口显示位置为紧贴屏幕上边界，保持置顶显示，无边框，不接受鼠标键盘事件，鼠标点击时不激活窗口，设置窗口穿透点击，窗口内容为对屏幕中心区域实时截图放大3倍。
2、使用dxcam作为截图库，截图区域为屏幕中心点周围宽度300正方形，帧率170。
3、使用指定库：pygame,dxcam,win32gui,win32con
'''

import pygame
import dxcam
import win32gui
import win32con

# 获取屏幕信息
screen = dxcam.create()
screen_width = screen.width
      
    
    
      
    
screen_height = screen.height

# 计算截图区域（屏幕中心300x300）
capture_size = 600#窗口宽度
magnify_times = 4 #放大倍率
left = (screen_width - capture_size) // 2
top = (screen_height - capture_size) // 2
region = (left, top, left + capture_size, top + capture_size)

# 初始化dxcam
fps=170
camera = dxcam.create(output_idx=0, output_color="RGB")
camera.start(region=region, target_fps=fps)

# 初始化Pygame窗口
pygame.init()
window_size = (capture_size, capture_size)
flags = pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF
screen = pygame.display.set_mode(window_size, flags)
hwnd = pygame.display.get_wm_info()["window"]

# 设置窗口属性
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) |
                       win32con.WS_EX_LAYERED |
                       win32con.WS_EX_TRANSPARENT |
                       win32con.WS_EX_TOPMOST)

win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST,
                      (screen_width - window_size[0]) // 2, 0,
                      window_size[0], window_size[1],
                      win32con.SWP_SHOWWINDOW)

# 主循环
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 获取并处理帧
    frame = camera.get_latest_frame()
    if frame is not None:
        # 转换为Pygame Surface
        img = pygame.image.frombuffer(frame, (capture_size, capture_size), 'RGB')
        
        # 放大3倍并裁剪中心区域
        scaled = pygame.transform.scale(img, (capture_size * magnify_times, capture_size * magnify_times))
        crop_rect = pygame.Rect(capture_size, capture_size, capture_size, capture_size)
        cropped = scaled.subsurface(crop_rect)
        
        # 更新窗口
        screen.blit(cropped, (0, 0))
        pygame.display.update()
    
    clock.tick(fps)

pygame.quit()
