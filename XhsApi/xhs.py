import pyautogui
import time

# 获取屏幕中心位置
screen_width, screen_height = pyautogui.size()
center_x = screen_width // 2
center_y = screen_height // 2

# 将鼠标移动到屏幕中心
pyautogui.moveTo(center_x, center_y)

# 设置滚动次数和间隔时间
scroll_count = 10000000000
scroll_delay = 0.5

# 开始滚动
for _ in range(scroll_count):
    pyautogui.scroll(-800)  # 向下滚动
    time.sleep(scroll_delay)