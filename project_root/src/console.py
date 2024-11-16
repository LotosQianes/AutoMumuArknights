import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import sys
import os


class Console:
    def __init__(self, root):
        self.root = root
        self.text_area = ScrolledText(root, wrap=tk.WORD, width=100, height=30)
        self.text_area.pack(expand=True, fill=tk.BOTH)
        self.text_area.configure(state=tk.DISABLED)

    def write(self, message):
        """将消息写入文本框"""
        self.text_area.configure(state=tk.NORMAL)
        self.text_area.insert(tk.END, message)
        self.text_area.configure(state=tk.DISABLED)
        self.text_area.see(tk.END)

    def flush(self):
        pass


def start_console():
    """启动控制台窗口"""
    root = tk.Tk()
    root.title("测试控制台")
    
    console = Console(root)
    sys.stdout = console
    sys.stderr = console
    
    root.mainloop()