import tkinter as tk
from pynput import mouse
import threading
import time

# 全局变量
scrolling = False
scroll_thread = None
last_x = 0
last_y = 0

class ScrollThread(threading.Thread):
    def __init__(self, direction, speed):
        super().__init__()
        self.direction = direction
        self.speed = speed
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            if self.direction == "up":
                mouse_controller.scroll(0, -self.speed)
            else:
                mouse_controller.scroll(0, self.speed)
            time.sleep(0.1)

def on_move(x, y):
    global scrolling, scroll_thread, last_x, last_y

    if scrolling:
        dx = abs(x - last_x)
        dy = abs(y - last_y)

        if dx > 10 or dy > 10:
            scrolling = False
            if scroll_thread:
                scroll_thread.running = False

    last_x = x
    last_y = y

def on_scroll(x, y, dx, dy):
    global scrolling, scroll_thread

    if not scrolling:
        scrolling = True
        scroll_thread = ScrollThread(scroll_direction.get(), scroll_speed.get())
        scroll_thread.start()

def start_scroll():
    global scrolling, scroll_thread
    if not scrolling:
        scrolling = True
        scroll_thread = ScrollThread(scroll_direction.get(), scroll_speed.get())
        scroll_thread.start()

def stop_scroll():
    global scrolling, scroll_thread
    scrolling = False
    if scroll_thread:
        scroll_thread.running = False

# 创建鼠标监听器
mouse_listener = mouse.Listener(on_move=on_move, on_scroll=on_scroll)
mouse_controller = mouse.Controller()

# 创建GUI窗口
root = tk.Tk()
root.title("自动滚动工具")

scroll_direction = tk.StringVar(value="up")
scroll_speed = tk.IntVar(value=1)

direction_label = tk.Label(root, text="滚动方向:")
direction_label.pack()

direction_radio_up = tk.Radiobutton(root, text="向下滚动", variable=scroll_direction, value="up")
direction_radio_up.pack()

direction_radio_down = tk.Radiobutton(root, text="向上滚动", variable=scroll_direction, value="down")
direction_radio_down.pack()

speed_label = tk.Label(root, text="滚动速度:")
speed_label.pack()

speed_scale = tk.Scale(root, variable=scroll_speed, from_=1, to=10, orient="horizontal")
speed_scale.pack()

start_button = tk.Button(root, text="开始滚动", command=start_scroll)
start_button.pack()

stop_button = tk.Button(root, text="移动停止", command=stop_scroll)
stop_button.pack()

# 启动鼠标监听
mouse_listener.start()

root.mainloop()
