from pynput import keyboard
import subprocess
import sys
import os

# 监听快捷键的组合
HOTKEY = {keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.Key.z}
current = set()

def on_press(key):
    global current
    try:
        current.add(key)
        if all(k in current for k in HOTKEY):
            print("\n✓ 快捷键触发！正在启动做题工具...\n")
            subprocess.Popen([sys.executable, 'quiz_solver.py'])
            current.clear()
    except AttributeError:
        pass

def on_release(key):
    global current
    try:
        current.discard(key)
    except AttributeError:
        pass

def main():
    print("=" * 50)
    print("快捷键监听器已启动")
    print("=" * 50)
    print("\n快捷键: Ctrl + Alt + Z")
    print("功能: 自动识别屏幕上的题目")
    print("\n按 Ctrl+C 停止监听\n")
    
    try:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except KeyboardInterrupt:
        print("\n\n监听器已关闭")

if __name__ == "__main__":
    main()
