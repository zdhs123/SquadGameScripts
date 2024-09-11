# from threading import Thread,Timer
import time
import keyboard
import mouse
from mouse._mouse_event import ButtonEvent, MoveEvent, WheelEvent, LEFT, RIGHT, MIDDLE, X, X2, UP, DOWN, DOUBLE


#放大镜
#58=caps lock,57=space,42=Shift,#55=Num*,74=Num-,78=Num+
mag_key=42
mag_triggrt_key=55
mag_zoomin_key=78
mag_zoomout_key=74
#临时放大限制
x_key='x'
v_key='v'
c_key='c'
z_key='z'
t_key='t'
f_key='f'
#小地图
smap_key=58
#大地图    
lmap_key='tab'
#标志位
if_smap_key_pressed=False
if_smap_showed=False
if_lmap_key_pressed=False
if_mag_key_pressed=False
if_x_key_pressed=False
if_v_key_pressed=False
if_magnified=False

keyboard.block_key(91)#禁用win键，防止跳出游戏
#keyboard.hook(lambda event:(print(event.name+":("+str(event.scan_code)+'):'+event.event_type )))#调试用显示按键码

while True:
    time.sleep(0.01)
#放大镜
    if keyboard.is_pressed(mag_key):
        if not if_mag_key_pressed:
            if_mag_key_pressed=True
            v_key_timestamp=time.time()

    elif if_mag_key_pressed and (not keyboard.is_pressed(mag_key)):
        if_mag_key_pressed=False
        
        if time.time()-v_key_timestamp<0.1:
            if not if_magnified:
                keyboard.send(mag_triggrt_key)
                if_magnified=True
            else:
                keyboard.send(mag_triggrt_key)
                if_magnified=False
            
#放大镜开启时，ZXC临时关闭放大
    if if_magnified:
        if (not if_x_key_pressed) and (keyboard.is_pressed(z_key) or keyboard.is_pressed(x_key) or keyboard.is_pressed(c_key) or keyboard.is_pressed(smap_key) or keyboard.is_pressed(lmap_key) or keyboard.is_pressed(t_key) or keyboard.is_pressed(f_key)):
            if_x_key_pressed=True
            keyboard.send(mag_triggrt_key)
        elif if_x_key_pressed and (not (keyboard.is_pressed(z_key) or keyboard.is_pressed(x_key) or keyboard.is_pressed(c_key) or keyboard.is_pressed(smap_key) or keyboard.is_pressed(lmap_key) or keyboard.is_pressed(t_key) or keyboard.is_pressed(f_key))):
            if_x_key_pressed=False
            keyboard.send(mag_triggrt_key)
#限制鼠标活动范围
    # if mouse.get_position()[1]<350:
    #     mouse.move(1269, 769, absolute=True, duration=0)
#小地图
    if keyboard.is_pressed(smap_key):
        if not if_smap_key_pressed:
            if_smap_key_pressed=True
            m_key_timestamp=time.time()
            if_smap_showed=True
        if time.time()-m_key_timestamp>1.5:#1.5秒关图
            if if_smap_showed:
                keyboard.send(smap_key)
                if_smap_showed=False
            
    elif if_smap_key_pressed and (not keyboard.is_pressed(smap_key)):
        if_smap_key_pressed=False
        if if_smap_showed:
            keyboard.send(smap_key)
            if_smap_showed=False

#大地图
    if (not if_lmap_key_pressed) and keyboard.is_pressed(lmap_key):
        if_lmap_key_pressed=True
    elif if_lmap_key_pressed and (not keyboard.is_pressed(lmap_key)):
        if_lmap_key_pressed=False
        keyboard.send(lmap_key)