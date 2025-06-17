from pynput import mouse, keyboard
import time
import winsound
import dxcam
import cv2 as cv
import numpy as np
import win32api, win32con
import psutil
import os

TILE_BGR = [0, 0, 0]


def select_game_border_points() -> list[2]:
    time.sleep(1.55)
    winsound.Beep(800, 50)
    xys = []
    def click_handler(x, y, button, pressed):
        nonlocal xys
        if button == mouse.Button.left and pressed:
            xys.append((x, y))
            if len(xys) >= 2:
                return False
    
    with mouse.Listener(on_click=click_handler) as listener:
        listener.join()
    
    
    winsound.Beep(800, 50)
    return xys[:2]

def get_frame(cam: dxcam.DXCamera, roi: tuple[2]):
    return cam.grab((*roi[0], *roi[1]))

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.005)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

    
def marked_spots(frame):
    h, w = frame.shape[:2]
    col_w = w//4
    for x in np.arange(0, w-col_w, col_w):
        x = x + col_w//2
        y = h//2

        cv.circle(frame, (x, y), 4, (0, 0, 255), 2)
    return frame


def start_cheat(cam: dxcam.DXCamera, roi: tuple[2]):
    p = psutil.Process(os.getpid())
    p.nice(psutil.HIGH_PRIORITY_CLASS)

    stop_cheat = False
    def on_press(key):
        nonlocal stop_cheat
        try:
            if key.char == 'q':
                print("Pressed 'q' — stopping cheat.")
                stop_cheat = True
                return False
        except AttributeError:
            pass
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    if cam.is_capturing:
        cam.stop()
        
    cam.start((*roi[0], *roi[1]), target_fps=120)
    winsound.Beep(800, 50)
    time.sleep(2)
    frame = cam.get_latest_frame()
    h, w = frame.shape[:2]
    col_w = w//4
    while True:
        frame = cam.get_latest_frame()
        
        for x in np.arange(0, w-col_w, col_w):
            x = x + col_w//2
            y = h//3*2
            if frame[y, x].tolist() == TILE_BGR:
                click(roi[0][0]+x, roi[0][1]+y)
        
        if stop_cheat:
            break
    
    winsound.Beep(800, 50)
    cam.stop()
    listener.stop()